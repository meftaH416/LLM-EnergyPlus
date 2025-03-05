import os
import json
import pandas as pd

# Step 1: Function to extract BuildingSurface:Detailed and FenestrationSurface:Detailed objects from an IDF file
def extract_objects(idf_file_path):
    with open(idf_file_path, 'r') as file:
        content = file.read()

    # Split the content into individual objects
    objects = content.split(';')
    building_surfaces = []
    fenestration_surfaces = []

    for obj in objects:
        if 'BuildingSurface:Detailed' in obj:
            # Clean up the object and add it to the list
            obj = obj.strip() + ';'  # Add back the semicolon
            building_surfaces.append(obj)
        elif 'FenestrationSurface:Detailed' in obj:
            # Clean up the object and add it to the list
            obj = obj.strip() + ';'  # Add back the semicolon
            fenestration_surfaces.append(obj)

    return building_surfaces, fenestration_surfaces

# Step 2: Read the Excel file
excel_file_path = 'building_descriptions.xlsx'  # Replace with your Excel file path
df = pd.read_excel(excel_file_path)

# Step 3: Create JSON pairs
json_pairs = []

# Iterate through each IDF file
idf_folder_path = 'path_to_idf_files'  # Replace with the folder containing your IDF files
for idf_file in os.listdir(idf_folder_path):
    if idf_file.endswith('.idf'):
        idf_file_path = os.path.join(idf_folder_path, idf_file)
        building_surfaces, fenestration_surfaces = extract_objects(idf_file_path)

        # Get the corresponding description from the Excel file
        building_id = int(idf_file.split('.')[0])  # Assuming the IDF file name is the ID (e.g., 1.idf)
        description = df[df['ID'] == building_id].iloc[0]

        # Create a JSON pair for each BuildingSurface:Detailed and FenestrationSurface:Detailed object
        for surface in building_surfaces:
            json_pair = {
                "user_query": f"Create IDF object BuildingSurface:Detailed with L={description['L']}, W={description['W']}, H={description['H']}, WWR={description['WWR']}, AR={description['AR']}",
                "answer": surface
            }
            json_pairs.append(json_pair)

        for surface in fenestration_surfaces:
            json_pair = {
                "user_query": f"Create IDF object FenestrationSurface:Detailed with L={description['L']}, W={description['W']}, H={description['H']}, WWR={description['WWR']}, AR={description['AR']}",
                "answer": surface
            }
            json_pairs.append(json_pair)

# Step 4: Save the JSON pairs to a file
output_json_path = 'building_and_fenestration_pairs.json'
with open(output_json_path, 'w') as json_file:
    json.dump(json_pairs, json_file, indent=4)

print(f"JSON pairs saved to {output_json_path}")
