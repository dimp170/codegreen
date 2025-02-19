import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datasets import load_from_disk
from tqdm import tqdm


dataset = load_from_disk("sonar_finetuning_dataset")


MODEL_NAME = "bigcode/starcoderbase"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype=torch.float16, device_map="auto")

def tokenize_function(example):
    return tokenizer(example["input"], text_target=example["output"], padding="max_length", truncation=True, max_length=1024)

dataset = dataset.map(tokenize_function, batched=True)


training_args = TrainingArguments(
    output_dir="./fine_tuned_model",
    evaluation_strategy="epoch",
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    save_total_limit=2,
    logging_dir="./logs",
    logging_steps=1,
    num_train_epochs=3,
    save_strategy="epoch",
    load_best_model_at_end=True
)


trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    tokenizer=tokenizer,
    data_collator=DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
)


total_steps = len(dataset) * training_args.num_train_epochs
progress_bar = tqdm(total=total_steps, desc="Training Progress")


for epoch in range(training_args.num_train_epochs):
    for step, batch in enumerate(trainer.get_train_dataloader()):
        trainer.model.train()
        loss = trainer.training_step(trainer.model, batch)
        progress_bar.update(1)
        progress_bar.set_postfix({"Loss": loss.item()})
        print(f"Step {step} | Epoch {epoch} | Loss: {loss.item():.4f}")
progress_bar.close()


model.save_pretrained("./optimized_code_model")
tokenizer.save_pretrained("./optimized_code_model")

print("Fine-tuning complete! Model saved in './optimized_code_model'.")
