import os
import json
import pandas as pd

# Function to extract BuildingSurface:Detailed and FenestrationSurface:Detailed objects from an IDF file
def extract_objects(idf_file_path):
    with open(idf_file_path, 'r') as file:
        content = file.read()

    # Split the content into individual objects
    objects = content.split(';')
    building_surfaces = []
    fenestration_surfaces = []

    for obj in objects:
        obj = obj.strip() + ';'  # Ensure semicolon is retained
        if 'BuildingSurface:Detailed' in obj:
            building_surfaces.append(obj)
        elif 'FenestrationSurface:Detailed' in obj:
            fenestration_surfaces.append(obj)

    return building_surfaces, fenestration_surfaces

# Define file paths
excel_file_path = 'building_descriptions.xlsx'  # Update as needed
idf_folder_path = 'path_to_idf_files'  # Update as needed
output_json_path = 'fine_tune_dataset.json'

# Load building descriptions
df = pd.read_excel(excel_file_path)

# Initialize JSON pairs list
json_pairs = []

# Process each IDF file
for idf_file in os.listdir(idf_folder_path):
    if idf_file.endswith('.idf'):
        idf_file_path = os.path.join(idf_folder_path, idf_file)
        building_surfaces, fenestration_surfaces = extract_objects(idf_file_path)

        # Get building description
        try:
            building_id = int(idf_file.split('.')[0])  # Assuming filename is ID (e.g., 1.idf)
            description = df[df['ID'] == building_id].iloc[0]
        except IndexError:
            print(f"Warning: No description found for {idf_file}")
            continue  # Skip if no matching description

        # Generate JSON pairs
        for surface in building_surfaces:
            json_pair = {
                "user_query": (
                    f"Create an EnergyPlus IDF object for a building surface with dimensions: "
                    f"Floor area of {FA}, L={description['L']}m, W={description['W']}m, H={description['H']}m, "
                    f"aspect ratio={description['AR']}, window-to-wall ratio={description['WWR']}. "
                    f"Ensure correct surface properties."
                ),
                "answer": surface
            }
            json_pairs.append(json_pair)

        for surface in fenestration_surfaces:
            json_pair = {
                "user_query": (
                    f"Create an EnergyPlus IDF object for a fenestration surface with dimensions: "
                    f"L={description['L']}m, W={description['W']}m, H={description['H']}m, "
                    f"aspect ratio={description['AR']}, window-to-wall ratio={description['WWR']}. "
                    f"Ensure correct placement on the building surface."
                ),
                "answer": surface
            }
            json_pairs.append(json_pair)

# Save dataset to JSON
with open(output_json_path, 'w') as json_file:
    json.dump(json_pairs, json_file, indent=4)

print(f"Fine-tuning dataset saved to {output_json_path}")
