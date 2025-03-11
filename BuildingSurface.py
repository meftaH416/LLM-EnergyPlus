import os
import json
import pandas as pd

# Function to extract BuildingSurface:Detailed and FenestrationSurface:Detailed objects from an IDF file
def extract_objects(idf_file_path):
    """Extracts BuildingSurface:Detailed and FenestrationSurface:Detailed objects from an IDF file."""
    with open(idf_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Split content into individual objects
    objects = content.split(';')
    
    # Extract relevant objects
    building_surfaces = [obj.strip() + ';' for obj in objects if 'BuildingSurface:Detailed' in obj]
    fenestration_surfaces = [obj.strip() + ';' for obj in objects if 'FenestrationSurface:Detailed' in obj]

    return building_surfaces, fenestration_surfaces

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
            
            FA = description.get("FA", "unknown")  # Handle missing values

        except ValueError:
            print(f"Skipping {idf_file} - Invalid filename format (expected 'in<ID>.idf')")
            continue  # Skip invalid filenames

        # Extract building and fenestration surfaces
        building_surfaces, fenestration_surfaces = extract_objects(idf_file_path)

        # Generate JSON pairs
        for surface in building_surfaces:
            json_pairs.append({
                "user": (
                    f"Create an EnergyPlus IDF object for a building surface with floor area {FA} m², "
                    f"L={description['L']}m, W={description['W']}m, H={description['H']}m, "
                    f"aspect ratio={description['AR']}, and WWR={description['WWR']}."
                ),
                "assistant": surface
            })

        for surface in fenestration_surfaces:
            json_pairs.append({
                "user": (
                    f"Create an EnergyPlus IDF object for a fenestration surface with dimensions "
                    f"L={description['L']}m, W={description['W']}m, H={description['H']}m, "
                    f"aspect ratio={description['AR']}, and WWR={description['WWR']}."
                ),
                "assistant": surface
            })

# Save dataset to JSON
with open(output_json_path, 'w', encoding='utf-8') as json_file:
    json.dump(json_pairs, json_file, indent=None, separators=(',', ':'))

print(f"Fine-tuning dataset saved to {output_json_path}")
