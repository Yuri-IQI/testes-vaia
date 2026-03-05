from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

load_in_8bit=True

class CodeAssistant:
    def __init__(self):
        model_name = "Qwen/Qwen2.5-Coder-1.5B-Instruct"

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype="auto",
            device_map="auto"
        )

    def generate_code(self, context: str, prompt: str):

        messages = [
            {"role": "system", "content": context},
            {"role": "user", "content": prompt}
        ]

        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        inputs = self.tokenizer(text, return_tensors="pt").to(self.model.device)

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=500
        )

        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    def parse_code(self, language: str, code: str):
        return code.split(f"```{language}")[-1].split("```")[0]