import os
import json
import pandas as pd
import random

def extract_idf_content(idf_path):
    """Reads the entire IDF file."""
    with open(idf_path, "r") as f:
        return f.read()

def generate_prompt(L, W, H, AR, WWR):
    """Generates diverse prompts for IDF creation."""
    prompt_templates = [
        f"Create an EnergyPlus IDF file for a rectangular building of floor are {FA} with L={L}, W={W}, height={H}, AR={AR}, WWR={WWR}, for a small office using ideal air HVAC.",
        f"Generate an IDF file for a rectangular small office of floor are {FA} with dimensions: L={L}, W={W}, H={H}, AR={AR}, WWR={WWR}. Use an ideal air HVAC system.",
        f"I need an IDF file for a small office of floor are {FA}: rectangular shape, dimensions L={L}, W={W}, H={H}, AR={AR}, WWR={WWR}, and an ideal air HVAC system.",
        f"Can you create an EnergyPlus IDF file for a regular size small office of floor are {FA} with length={L} by width={W} by height={H}, aspect ratio {AR}, and WWR={WWR}?",
        f"Small office of floor {FA}, rectangular (length of {L}, width of {W} by height {H}, AR={AR} and WWR={WWR}), ideal air HVAC – create an IDF file."
    ]
    return random.choice(prompt_templates)

def create_idf_json(idf_folder, excel_file, output_json):
    """Creates JSON with full IDF file as answer and structured user prompt."""
    df = pd.read_excel(excel_file)
    data_pairs = []
    
    for index, row in df.iterrows():
        # Extract values from Excel
        ID = str(row["ID"])  # Ensure ID is a string for matching
        L, W, H, AR, WWR = row["L"], row["W"], row["H"], row["AR"], row["WWR"]

        # Generate a random prompt
        user_prompt = generate_prompt(L, W, H, AR, WWR)

        # Find the corresponding IDF file
        matched_idf = None
        for idf_file in os.listdir(idf_folder):
            if idf_file.endswith(f"{ID}.idf"):  # Match filename ending with ID
                idf_path = os.path.join(idf_folder, idf_file)
                matched_idf = extract_idf_content(idf_path)
                break  # Stop after finding the first match

        answer = matched_idf if matched_idf else "No matching IDF found."
        data_pairs.append({"user": user_prompt, "answer": answer})

    # Save as JSON
    with open(output_json, "w") as f:
        json.dump(data_pairs, f, indent=4)

# Example usage
idf_folder = "path_to_idf_files"  # Folder where IDF files are stored
excel_file = "path_to_excel.xlsx"  # Excel file containing building parameters
output_json = "idf_dataset.json"  # Output JSON file

create_idf_json(idf_folder, excel_file, output_json)
