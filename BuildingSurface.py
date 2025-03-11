import os
import json
import pandas as pd
import random

# Function to extract BuildingSurface:Detailed and FenestrationSurface:Detailed objects
def extract_objects(idf_file_path):
    """Extracts BuildingSurface:Detailed and FenestrationSurface:Detailed objects from an IDF file."""
    with open(idf_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    objects = content.split(';')
    
    building_surfaces = [obj.strip() + ';' for obj in objects if 'BuildingSurface:Detailed' in obj]
    fenestration_surfaces = [obj.strip() + ';' for obj in objects if 'FenestrationSurface:Detailed' in obj]

    return building_surfaces, fenestration_surfaces

# Function to generate a randomized user query combining both surfaces
def generate_combined_query(description):
    """Returns a user query asking for both a building surface and a fenestration surface."""
    templates = [
        f"Create an EnergyPlus IDF object for a building surface and its fenestration (window/aperture) with floor area {description['FA']} m², "
        f"L={description['L']}m, W={description['W']}m, H={description['H']}m, AR={description['AR']}, WWR={description['WWR']}. Ensure correct placement.",

        f"Generate an IDF file defining both a building surface and its associated fenestration surface (window or aperture) for a building with "
        f"{description['FA']} m² floor area, dimensions {description['L']}m x {description['W']}m x {description['H']}m, aspect ratio {description['AR']}, and WWR {description['WWR']}.",

        f"Provide an EnergyPlus IDF component that includes a building surface and its corresponding window or aperture with dimensions: "
        f"L={description['L']}m, W={description['W']}m, H={description['H']}m, AR={description['AR']}, and WWR={description['WWR']}."
    ]
    return random.choice(templates)

# Define file paths
excel_file_path = 'data.csv'  # Update as needed
idf_folder_path = 'path_to_idf_files'  # Update as needed
output_json_path = 'fine_tune_dataset.json'

# Load building descriptions
if not os.path.exists(excel_file_path):
    raise FileNotFoundError(f"CSV file not found: {excel_file_path}")

df = pd.read_csv(excel_file_path)

# Convert ID column to dictionary for fast lookup
building_data = df.set_index('ID').to_dict(orient='index')

# Initialize JSON pairs list
json_pairs = []

# Process each IDF file
for idf_file in os.listdir(idf_folder_path):
    if idf_file.endswith('.idf') and idf_file.startswith("in"):
        idf_file_path = os.path.join(idf_folder_path, idf_file)

        # Extract numeric building ID (e.g., "in1.idf" → 1)
        try:
            building_id = int(idf_file.replace("in", "").replace(".idf", ""))
            description = building_data.get(building_id)

            if not description:
                print(f"Warning: No description found for {idf_file}")
                continue  # Skip if no matching description

        except ValueError:
            print(f"Skipping {idf_file} - Invalid filename format (expected 'in<ID>.idf')")
            continue  # Skip invalid filenames

        # Extract building and fenestration surfaces
        building_surfaces, fenestration_surfaces = extract_objects(idf_file_path)

        # Ensure both surface types exist before creating a dataset entry
        if building_surfaces and fenestration_surfaces:
            json_pairs.append({
                "user": generate_combined_query(description),
                "assistant": "\n".join(building_surfaces + fenestration_surfaces)
            })

# Save dataset to JSON
with open(output_json_path, 'w', encoding='utf-8') as json_file:
    json.dump(json_pairs, json_file, indent=None, separators=(',', ':'))

print(f"Fine-tuning dataset saved to {output_json_path}")
