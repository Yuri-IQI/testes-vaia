from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Optional

import torch
from datasets import Dataset
from peft import LoraConfig, get_peft_model, TaskType, PeftModel
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer
)
from trl import SFTTrainer, SFTConfig

BASE_MODEL = os.getenv("TRAIN_MODEL", "Qwen/Qwen2.5-0.5B-Instruct")
DEFAULT_ADAPTER = os.getenv("DEFAULT_ADAPTER", "financial_adapter")

@dataclass
class FinancialFineTuneConfig:
    base_model_name: str = BASE_MODEL
    output_dir: str = "./" + DEFAULT_ADAPTER

    use_4bit: bool = True
    bnb_4bit_compute_dtype: str = "float16"
    bnb_4bit_quant_type: str = "nf4"

    lora_r: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.05

    target_modules: list[str] = field(
        default_factory=lambda: ["q_proj", "k_proj", "v_proj", "o_proj"]
    )

    num_train_epochs: int = 3
    per_device_train_batch_size: int = 4
    gradient_accumulation_steps: int = 4
    learning_rate: float = 2e-4
    max_seq_length: int = 512
    warmup_ratio: float = 0.03
    lr_scheduler_type: str = "cosine"


class FinancialModelTrainer:
    def __init__(self, config: FinancialFineTuneConfig) -> None:
        self.config = config
        self._model = None
        self._tokenizer = None

    def _load_base_model(self) -> None:
        cfg = self.config

        self._tokenizer = AutoTokenizer.from_pretrained(cfg.base_model_name)
        self._tokenizer.pad_token = self._tokenizer.eos_token
        self._tokenizer.padding_side = "right"

        self._model = AutoModelForCausalLM.from_pretrained(
            cfg.base_model_name,
            dtype=torch.float16,
            device_map="auto",
        )
        self._model.config.use_cache = False
        
    def _apply_lora(self) -> None:
        cfg = self.config
        lora_config = LoraConfig(
            r=cfg.lora_r,
            lora_alpha=cfg.lora_alpha,
            target_modules=cfg.target_modules,
            lora_dropout=cfg.lora_dropout,
            bias="none",
            task_type=TaskType.CAUSAL_LM,
        )
        self._model = get_peft_model(self._model, lora_config)
        self._model.print_trainable_parameters()

    def train(self, dataset: Dataset) -> None:
        self._load_base_model()
        self._apply_lora()

        cfg = self.config
        
        is_cuda = torch.cuda.is_available()

        training_args = SFTConfig(
            output_dir=cfg.output_dir,
            num_train_epochs=cfg.num_train_epochs,
            per_device_train_batch_size=cfg.per_device_train_batch_size,
            gradient_accumulation_steps=cfg.gradient_accumulation_steps,
            learning_rate=cfg.learning_rate,
            logging_steps=10,
            save_strategy="epoch",
            warmup_ratio=cfg.warmup_ratio,
            lr_scheduler_type=cfg.lr_scheduler_type,
            report_to="none",
            dataset_text_field="text",
            max_length=cfg.max_seq_length,
            packing=False,
            use_cpu=not is_cuda, 
            dataloader_num_workers=0, 
            fp16=True,
            gradient_checkpointing=True,
        )

        trainer = SFTTrainer(
            model=self._model,
            train_dataset=dataset,
            args=training_args,
            processing_class=self._tokenizer,
        )

        trainer.train()
        trainer.save_model(cfg.output_dir)
        self._tokenizer.save_pretrained(cfg.output_dir)
        print(f"Modelo salvo em: {cfg.output_dir}")
        