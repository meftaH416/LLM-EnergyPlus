import json
import random
from datasets import DatasetDict, Dataset

# Load the generated dataset
with open("MainPrompt.json", "r") as f:
    data = json.load(f)

# Shuffle the dataset to ensure randomness
random.shuffle(data)

# Define split ratios
train_ratio = 0.9
val_ratio = 0.05
test_ratio = 0.05

# Compute split sizes
total_size = len(data)
train_size = int(train_ratio * total_size)
val_size = int(val_ratio * total_size)
test_size = total_size - train_size - val_size  # Ensure exact split

# Split dataset
train_data = data[:train_size]
val_data = data[train_size:train_size + val_size]
test_data = data[train_size + val_size:]

# Save as separate JSON files in the main folder
with open("train.json", "w") as f:
    json.dump(train_data, f, indent=2)

with open("val.json", "w") as f:
    json.dump(val_data, f, indent=2)

with open("test.json", "w") as f:
    json.dump(test_data, f, indent=2)

print(f"Dataset split into Train: {train_size}, Val: {val_size}, Test: {test_size}")

# Convert to Hugging Face Dataset format
dataset = DatasetDict({
    "train": Dataset.from_list(train_data),
    "validation": Dataset.from_list(val_data),
    "test": Dataset.from_list(test_data),
})

# Save as Hugging Face Dataset (optional)
dataset.save_to_disk("MainPrompt")
print("Hugging Face dataset saved as 'MainPrompt'")
