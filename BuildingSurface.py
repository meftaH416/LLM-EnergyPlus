import os
import json
import pandas as pd
import random

# Function to extract EnergyPlus objects with strict name matching
def extract_objects(idf_file_path):
    """Extracts strictly matching Zone, Space, SpaceList, BuildingSurface:Detailed, and FenestrationSurface:Detailed objects."""
    with open(idf_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    current_obj = []
    # extracted_objects = {key: [] for key in [ "Zone,", "Space,", "SpaceList,", "BuildingSurface:Detailed,", "FenestrationSurface:Detailed,"]}
    extracted_objects = {key: [] for key in ["Zone,", "Space,", "SpaceList,", "BuildingSurface:Detailed,", "FenestrationSurface:Detailed,"]}

    inside_object = None  # Track current object type

    for line in lines:
        stripped_line = line.strip()
        if not stripped_line:
            continue  # Skip empty lines

        # Normalize spacing and remove excessive gaps
        clean_line = " ".join(stripped_line.split())  
        clean_line = clean_line.replace(" ,", ",").replace(", ", ",")  # Ensure proper comma spacing

        # Detect new object start
        for key in extracted_objects.keys():
            if clean_line.startswith(key):
                inside_object = key  # Set current object type
                current_obj = [clean_line]  # Start new object
                break
        else:
            # If already inside an object, continue collecting lines
            if inside_object:
                current_obj.append(clean_line)

        # If line ends with ';', complete the object
        if ";" in clean_line and inside_object:
            extracted_objects[inside_object].append("\n".join(current_obj))
            inside_object = None  # Reset tracking variable

    return [extracted_objects[key] for key in extracted_objects]

# Function to generate a user query
def generate_combined_query(description):
    """Returns a user query asking for a Zone, Space, SpaceList, BuildingSurface, and FenestrationSurface."""
    templates = [
        f"Create an EnergyPlus IDF component including a Zone, Space, and SpaceList along with a building surface and its fenestration.\n"
        f"Building details: FA={description['FA']} ft2, L={description['L']} ft, W={description['W']} ft, H={description['H']}ft, AR={description['AR']}, WWR={description['WWR']}.",

        f"Generate an IDF snippet defining a Zone, Space, SpaceList, a building surface, and an associated window/aperture.\n"
        f"Building: {description['FA']} ft2, {description['L']}ft x {description['W']}ft x {description['H']}ft, AR={description['AR']}, WWR={description['WWR']}.",

        f"Provide an EnergyPlus IDF file that includes a Zone, Space, SpaceList, a building surface, and a window/aperture.\n"
        f"Details: L={description['L']}ft, W={description['W']}ft, H={description['H']}ft, AR={description['AR']}, WWR={description['WWR']}.",

        f"Give me EnergyPlus IDF file that includes a Zone, Space, SpaceList, a building surface, and a window/aperture.\n"
        f"Details: L={description['L']}ft, W={description['W']}ft, H={description['H']}ft, AR={description['AR']}, WWR={description['WWR']}.",

        f"Make IDF defining a Zone, Space, SpaceList, a building surface, and an associated window.\n"
        f"Building: {description['FA']} ft2, {description['L']}ft x {description['W']}ft x {description['H']}ft, AR={description['AR']}, WWR={description['WWR']}.",
        f"Construct an EnergyPlus IDF file featuring a Zone, Space, SpaceList, a building surface, and its fenestration.\n"
        f"Specifications: Floor Area={description['FA']} ft², Length={description['L']} ft, Width={description['W']} ft, Height={description['H']} ft, Aspect Ratio={description['AR']}, Window-to-Wall Ratio={description['WWR']}.",
    
        f"Draft an IDF file that includes a Zone, Space, SpaceList, a primary building surface, and a window or other fenestration element.\n"
        f"Building properties: {description['FA']} ft² total, {description['L']} ft x {description['W']} ft x {description['H']} ft, AR={description['AR']}, WWR={description['WWR']}.",
    
        f"Generate an EnergyPlus IDF section containing a Zone, Space, SpaceList, a surface with an aperture, and necessary geometric details.\n"
        f"Dimensions: {description['L']} ft (L) x {description['W']} ft (W) x {description['H']} ft (H), Total Area={description['FA']} ft², AR={description['AR']}, WWR={description['WWR']}.",
    
        f"Create a valid IDF file for EnergyPlus that defines a Zone, Space, SpaceList, a building envelope surface, and an opening such as a window.\n"
        f"Given parameters: FA={description['FA']} ft², L={description['L']} ft, W={description['W']} ft, H={description['H']} ft, AR={description['AR']}, WWR={description['WWR']}.",
    
        f"Write an IDF script containing a Zone, Space, SpaceList, an exterior surface, and its corresponding fenestration.\n"
        f"Input specifications: Floor Area={description['FA']} ft², Length={description['L']} ft, Width={description['W']} ft, Height={description['H']} ft, AR={description['AR']}, WWR={description['WWR']}.",
        
        f"Design an IDF file that incorporates a Zone, Space, SpaceList, a key building surface, and its fenestration for EnergyPlus simulation.\n"
        f"Parameters: Floor Area={description['FA']} ft², L={description['L']} ft, W={description['W']} ft, H={description['H']} ft, AR={description['AR']}, WWR={description['WWR']}.",
    
        f"Prepare an EnergyPlus IDF definition that includes a Zone, Space, SpaceList, an exterior wall, and an associated window or aperture.\n"
        f"Building configuration: {description['FA']} ft², {description['L']} ft x {description['W']} ft x {description['H']} ft, AR={description['AR']}, WWR={description['WWR']}.",
    
        f"Write an IDF file for a building with a Zone, Space, SpaceList, a primary surface, and an opening for EnergyPlus analysis.\n"
        f"Specifications: L={description['L']} ft, W={description['W']} ft, H={description['H']} ft, FA={description['FA']} ft², AR={description['AR']}, WWR={description['WWR']}.",
    
        f"Develop an EnergyPlus IDF file that defines a Zone, Space, SpaceList, a wall with a fenestration element, and other necessary details.\n"
        f"Inputs: Floor Area={description['FA']} ft², Length={description['L']} ft, Width={description['W']} ft, Height={description['H']} ft, AR={description['AR']}, WWR={description['WWR']}.",
    
        f"Formulate an IDF snippet that includes a Zone, Space, SpaceList, a structural surface, and a window or glazing element.\n"
        f"Building parameters: {description['FA']} ft² total, Dimensions: {description['L']} ft x {description['W']} ft x {description['H']} ft, AR={description['AR']}, WWR={description['WWR']}.",

        f"How can I generate an EnergyPlus IDF file that includes a Zone, Space, SpaceList, a building surface, and a window?\n"
        f"My building details are: Floor Area={description['FA']} ft², Length={description['L']} ft, Width={description['W']} ft, Height={description['H']} ft, Aspect Ratio={description['AR']}, and Window-to-Wall Ratio={description['WWR']}.",
    
        f"Can you provide an IDF file containing a Zone, Space, SpaceList, an exterior surface, and its fenestration?\n"
        f"The building parameters are: {description['FA']} ft² total, {description['L']} ft x {description['W']} ft x {description['H']} ft, AR={description['AR']}, WWR={description['WWR']}.",
    
        f"What would an EnergyPlus IDF look like for a building with a Zone, Space, SpaceList, a primary surface, and a window?\n"
        f"Here are my specifications: L={description['L']} ft, W={description['W']} ft, H={description['H']} ft, FA={description['FA']} ft², AR={description['AR']}, WWR={description['WWR']}.",
    
        f"Can you help me create an IDF snippet for EnergyPlus that includes a Zone, Space, SpaceList, a structural surface, and a glazing element?\n"
        f"The building details are: {description['FA']} ft², Dimensions: {description['L']} ft x {description['W']} ft x {description['H']} ft, AR={description['AR']}, WWR={description['WWR']}.",
    
        f"What is the correct IDF structure for defining a Zone, Space, SpaceList, an exterior wall, and a window in EnergyPlus?\n"
        f"My building specifications are: Floor Area={description['FA']} ft², Length={description['L']} ft, Width={description['W']} ft, Height={description['H']} ft, AR={description['AR']}, WWR={description['WWR']}.",
    ]
    return random.choice(templates)

# Define file paths
excel_file_path = r'C:\Users\\Desktop\LLM Eplus\idf_rectangle\data.csv'
idf_folder_path = r'C:\Users\\Desktop\LLM Eplus\idf_rectangle'
output_json_path = 'BuildingGeometricDataset.json'

# Load building descriptions
if not os.path.exists(excel_file_path):
    raise FileNotFoundError(f"CSV file not found: {excel_file_path}")

df = pd.read_csv(excel_file_path)
building_data = df.set_index('ID').to_dict(orient='index')

# Initialize JSON pairs list
json_pairs = []

# Process each IDF file
for idf_file in os.listdir(idf_folder_path):
    if idf_file.endswith('.idf') and idf_file.startswith("in"):
        idf_file_path = os.path.join(idf_folder_path, idf_file)

        try:
            building_id = int(idf_file.replace("in", "").replace(".idf", ""))
            description = building_data.get(building_id)
            if not description:
                print(f"Warning: No description found for {idf_file}")
                continue
        except ValueError:
            print(f"Skipping {idf_file} - Invalid filename format.")
            continue

        # Extract EnergyPlus objects
        zones, spaces, space_lists, building_surfaces, fenestration_surfaces = extract_objects(idf_file_path)

        # Debugging: Print number of extracted components
        print(f"Processing {idf_file}: Zones({len(zones)}), Spaces({len(spaces)}), "
              f"SpaceLists({len(space_lists)}), Surfaces({len(building_surfaces)}), Windows({len(fenestration_surfaces)})")

        # Ensure at least some components exist
        if any([zones, spaces, space_lists, building_surfaces, fenestration_surfaces]):
            json_pairs.append({
                "user": generate_combined_query(description),
                "assistant": "\n".join(zones + spaces + space_lists + building_surfaces + fenestration_surfaces)
            })
        else:
            print(f"Skipping {idf_file} - No relevant objects found.")

# Save dataset to JSON
with open(output_json_path, 'w', encoding='utf-8') as json_file:
    json.dump(json_pairs, json_file, indent=2)

print(f"Fine-tuning dataset saved to {output_json_path}")
