from datasets import Dataset
from examples import format_for_training
from fine_tuner import FinancialModelTrainer, FinancialFineTuneConfig

formatted = format_for_training()
print(f"Exemplos: {len(formatted)}")

dataset = Dataset.from_list(formatted)

config = FinancialFineTuneConfig(
    output_dir="./desenrola_model_1.5B",
    base_model_name="Qwen/Qwen2.5-1.5B-Instruct",
    use_4bit=False,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=8,
    max_seq_length=512,
    lora_r=8,
    num_train_epochs=10,
)

trainer = FinancialModelTrainer(config)
trainer.train(dataset)