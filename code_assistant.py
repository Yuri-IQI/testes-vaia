from transformers import AutoModelForCausalLM, AutoTokenizer
import json
import torch
import re

load_in_8bit=True

class CodeAssistant:
    def __init__(self):
        model_name = "Qwen/Qwen2.5-Coder-1.5B-Instruct"

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            dtype=torch.float32,
            device_map="auto"
        )

    def generate_code(self, context: str, prompt: str):

        messages = [
            {"role": "system", "content": context},
            {"role": "user", "content": prompt}
        ]

        inputs = self.tokenizer(prompt, return_tensors="pt")

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=300,
            temperature=0.1,
            do_sample=True,
            top_p=0.9,
            eos_token_id=self.tokenizer.convert_tokens_to_ids("}")
        )

        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)