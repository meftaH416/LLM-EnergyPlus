import os
import json
import pandas as pd
import random

def extract_idf_content(idf_path):
    """Reads the entire IDF file."""
    with open(idf_path, "r") as f:
        return f.read()

def generate_prompt(FA, L, W, H, AR, WWR):
    """Generates diverse prompts for IDF creation."""
    prompt_templates = [
        f"Create an EnergyPlus IDF file for a rectangular building of floor area {FA} with L={L}, W={W}, height={H}, AR={AR}, WWR={WWR}, for a small office using ideal air HVAC.",
        f"Generate an IDF file for a rectangular small office of floor area {FA} with dimensions: L={L}, W={W}, H={H}, AR={AR}, WWR={WWR}. Use an ideal air HVAC system.",
        f"I need an IDF file for a small office of floor area {FA}: rectangular shape, dimensions L={L}, W={W}, H={H}, AR={AR}, WWR={WWR}, and an ideal air HVAC system.",
        f"Can you create an EnergyPlus IDF file for a regular-size small office of floor area {FA} with length={L} by width={W} by height={H}, aspect ratio {AR}, and WWR={WWR}?",
        f"Small office of floor {FA}, rectangular (length of {L}, width of {W}, height {H}, AR={AR}, and WWR={WWR}), ideal air HVAC - create an IDF file."
    ]
    return random.choice(prompt_templates)

def create_idf_json(idf_folder, csv_file, output_json):
    """Creates JSON with full IDF file as answer and structured user prompt."""
    df = pd.read_csv(csv_file)
    data_pairs = []
    
    # Pre-load all IDF filenames into a set for fast lookup
    idf_files = {f.lower().strip() for f in os.listdir(idf_folder) if f.endswith(".idf")}

    for index, row in df.iterrows():
        # Extract values from CSV
        ID = "in" + str(int(row["ID"])).strip().lower()  # Normalize ID
        FA, L, W, H, AR, WWR = row["FA"], row["L"], row["W"], row["H"], row["AR"], row["WWR"]

        # Generate a random prompt
        user_prompt = generate_prompt(FA, L, W, H, AR, WWR)

        # Remove extra spaces from the user prompt
        user_prompt = ' '.join(user_prompt.split())

        # Find the corresponding IDF file
        idf_filename = f"{ID}.idf"
        idf_path = os.path.join(idf_folder, idf_filename)

        # Extract content if file exists
        answer = extract_idf_content(idf_path) if idf_filename in idf_files else "No matching IDF found."

        # Remove extra spaces from the answer
        answer = ' '.join(answer.split())

        data_pairs.append({"user": user_prompt, "answer": answer})

    # Save as JSON with a compact indentation (2 spaces)
    with open(output_json, "w") as f:
        json.dump(data_pairs, f, indent=2)

# Example usage
idf_folder = r"C:\Users\\Desktop\LLM Eplus\idf_rectangle"
csv_file = r"C:\Users\\Desktop\LLM Eplus\idf_rectangle\data.csv"
output_json = "idf_rectangle_dataset.json"

create_idf_json(idf_folder, csv_file, output_json)

# print("Available IDF Files:", os.listdir(idf_folder))
