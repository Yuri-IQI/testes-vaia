from __future__ import annotations

import os
from typing import Optional

try:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
except Exception:
    AutoModelForCausalLM = None
    AutoTokenizer = None
    torch = None

DEFAULT_MODEL_NAME = os.getenv("BASE_MODEL", "Qwen/Qwen2.5-Coder-1.5B-Instruct")

class CodeAssistant:
    def __init__(self, model_name: str = DEFAULT_MODEL_NAME) -> None:
        self.model_name = model_name
        self._tokenizer = None
        self._model = None
        self._load_error: Optional[str] = None

    @property
    def load_error(self) -> Optional[str]:
        return self._load_error

    @property
    def is_ready(self) -> bool:
        return self._tokenizer is not None and self._model is not None

    def _ensure_loaded(self) -> None:
        if self.is_ready:
            return

        if AutoTokenizer is None or AutoModelForCausalLM is None or torch is None:
            self._load_error = "transformers and torch are not available in this environment."
            raise RuntimeError(self._load_error)

        try:
            dtype = torch.float16 if torch.cuda.is_available() else torch.float32
            self._tokenizer = AutoTokenizer.from_pretrained(self.model_name)

            model_kwargs = {"torch_dtype": dtype}
            if torch.cuda.is_available():
                model_kwargs["device_map"] = "auto"

            self._model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                **model_kwargs,
            )
            self._load_error = None
        except Exception as exc:
            self._tokenizer = None
            self._model = None
            self._load_error = str(exc)
            raise RuntimeError(
                f"Could not load model '{self.model_name}'. "
                "Install the project dependencies and make the model available locally."
            ) from exc

    def generate_text(
        self,
        system_prompt: str,
        user_prompt: str,
        *,
        max_new_tokens: int = 300,
        temperature: float = 0.1,
        top_p: float = 0.9,
    ) -> str:
        self._ensure_loaded()

        assert self._tokenizer is not None
        assert self._model is not None

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        if hasattr(self._tokenizer, "apply_chat_template"):
            prompt_text = self._tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True,
            )
        else:
            prompt_text = f"System:\n{system_prompt}\n\nUser:\n{user_prompt}\n\nAssistant:\n"

        inputs = self._tokenizer(prompt_text, return_tensors="pt")
        
        model_device = next(self._model.parameters()).device
        inputs = {key: value.to(model_device) for key, value in inputs.items()}

        outputs = self._model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            do_sample=temperature > 0,
            top_p=top_p,
            pad_token_id=self._tokenizer.eos_token_id,
        )
    
        generated_tokens = outputs[0][inputs["input_ids"].shape[-1] :]
        return self._tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()
