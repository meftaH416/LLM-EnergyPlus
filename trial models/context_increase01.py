# Install required libraries
!pip install transformers datasets accelerate

# Import libraries
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
from datasets import load_dataset
import torch

# Step 1: Load the DeepSeek-R1-Distill-Qwen-1.5B model and tokenizer
model_name = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Step 2: Modify the model's configuration to support longer sequences
# Check the current max position embeddings
print(f"Original max position embeddings: {model.config.max_position_embeddings}")

# Increase the max position embeddings to 10,000
model.config.max_position_embeddings = 10000

# Resize the token embeddings to match the new max position embeddings
model.resize_token_embeddings(len(tokenizer))

# Verify the change
print(f"Updated max position embeddings: {model.config.max_position_embeddings}")

# Step 3: Fine-tune the model (optional)
# Load a dataset for fine-tuning
dataset = load_dataset("wikitext", "wikitext-2-raw-v1")  # Example dataset

# Tokenize the dataset
def tokenize_function(examples):
    return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=2048)  # Reduce max_length for memory efficiency

tokenized_datasets = dataset.map(tokenize_function, batched=True)

# Set up training arguments with memory optimization
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=1,  # Reduce batch size to fit in memory
    per_device_eval_batch_size=1,
    gradient_accumulation_steps=4,  # Accumulate gradients to simulate larger batch size
    num_train_epochs=1,
    weight_decay=0.01,
    save_total_limit=2,
    fp16=True,  # Enable mixed precision training to save memory
    logging_dir="./logs",
    logging_steps=10,
)

# Initialize the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"],
)

# Fine-tune the model
trainer.train()

# Save the fine-tuned model
model.save_pretrained("./fine-tuned-deepseek-r1")
tokenizer.save_pretrained("./fine-tuned-deepseek-r1")

# Step 4: Generate longer outputs
# Load the fine-tuned model (if you fine-tuned it)
model = AutoModelForCausalLM.from_pretrained("./fine-tuned-deepseek-r1")
tokenizer = AutoTokenizer.from_pretrained("./fine-tuned-deepseek-r1")

# Generate text with a longer sequence length
input_text = "Once upon a time"
input_ids = tokenizer(input_text, return_tensors="pt").input_ids

# Generate up to 10,000 tokens in chunks to avoid memory issues
max_length = 10000
chunk_size = 2048  # Process in smaller chunks
output_ids = input_ids

for _ in range(max_length // chunk_size):
    output_ids = model.generate(
        output_ids,
        max_length=output_ids.shape[1] + chunk_size,
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        do_sample=True,
        top_p=0.95,
        temperature=0.7,
    )

# Decode the generated text
generated_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
print(generated_text)
