import os

from datasets import Dataset
from examples import format_for_training
from fine_tuner import FinancialModelTrainer, FinancialFineTuneConfig

DEFAULT_MODEL_NAME = os.getenv("TRAIN_MODEL", "Qwen/Qwen2.5-Coder-0.5B-Instruct")
DEFAULT_ADAPTER = os.getenv("v", "financial_adapter")

formatted = format_for_training()
print(f"Exemplos: {len(formatted)}")

dataset = Dataset.from_list(formatted)

config = FinancialFineTuneConfig(
    output_dir="./" + DEFAULT_ADAPTER,
    base_model_name=DEFAULT_MODEL_NAME,
    use_4bit=False,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=8,
    max_seq_length=512,
    lora_r=8,
    num_train_epochs=10,
)

trainer = FinancialModelTrainer(config)
trainer.train(dataset)