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
            # Join the current object lines with spaces, then add a newline after the semicolon
            complete_object = " ".join(current_obj)
            extracted_objects[inside_object].append(complete_object)
            inside_object = None  # Reset tracking variable

    return [extracted_objects[key] for key in extracted_objects]

# Function to generate a user query
def generate_combined_query(description):
    """Returns a user query asking for a Zone, Space, SpaceList, BuildingSurface, and FenestrationSurface."""
    templates = [
        f"Create an EnergyPlus IDF component including a Zone, Space, and SpaceList along with a building surface and its fenestration."
        f"Building details: FA={description['FA']:.1f} ft2, L={description['L']:.1f} ft, W={description['W']:.1f} ft, H={description['H']:.1f}ft, AR={description['AR']:.1f}, WWR={description['WWR']:.1f}.",

        f"Generate an IDF snippet defining a Zone, Space, SpaceList, a building surface, and an associated window/aperture."
        f"Building: {description['FA']:.1f} ft2, {description['L']:.1f}ft x {description['W']:.1f}ft x {description['H']:.1f}ft, AR={description['AR']:.1f}, WWR={description['WWR']:.1f}.",

        f"Provide an EnergyPlus IDF file that includes a Zone, Space, SpaceList, a building surface, and a window/aperture."
        f"Details: L={description['L']:.1f}ft, W={description['W']:.1f}ft, H={description['H']:.1f}ft, AR={description['AR']:.1f}, WWR={description['WWR']:.1f}.",

        f"Give me EnergyPlus IDF file that includes a Zone, Space, SpaceList, a building surface, and a window/aperture."
        f"Details: L={description['L']:.1f}ft, W={description['W']:.1f}ft, H={description['H']:.1f}ft, AR={description['AR']:.1f}, WWR={description['WWR']:.1f}.",

        f"Make IDF defining a Zone, Space, SpaceList, a building surface, and an associated fenestration."
        f"Building: {description['FA']:.1f} ft2, {description['L']:.1f}ft x {description['W']:.1f}ft x {description['H']:.1f}ft, AR={description['AR']:.1f}, WWR={description['WWR']:.1f}.",
        f"Construct an EnergyPlus IDF file featuring a Zone, Space, SpaceList, a building surface, and its fenestration.\n"
        f"Specifications: Floor Area={description['FA']:.1f} sq.ft, Length={description['L']:.1f} ft, Width={description['W']:.1f} ft, Height={description['H']:.1f} ft, Aspect Ratio={description['AR']:.1f}, Window-to-Wall Ratio={description['WWR']:.1f}.",
    
        f"Draft an IDF file that includes a Zone, Space, SpaceList, a building surface, and a window or other fenestration element."
        f"Building properties: {description['FA']:.1f} sq.ft total, {description['L']:.1f} ft x {description['W']:.1f} ft x {description['H']:.1f} ft, AR={description['AR']:.1f}, WWR={description['WWR']:.1f}.",
    
        f"Generate an EnergyPlus IDF section containing a Zone, Space, SpaceList, a building surface with fenestration, and necessary geometric details."
        f"Dimensions: {description['L']:.1f} ft (L) x {description['W']:.1f} ft (W) x {description['H']:.1f} ft (H), Total Area={description['FA']:.1f} sq.ft, AR={description['AR']:.1f}, WWR={description['WWR']:.1f}.",
    
        f"Create a valid IDF file for EnergyPlus that defines a Zone, Space, SpaceList, a building envelope surface, and an opening such as a window."
        f"Given parameters: FA={description['FA']:.1f} square ft, L={description['L']:.1f} ft, W={description['W']:.1f} ft, H={description['H']:.1f} ft, AR={description['AR']:.1f}, WWR={description['WWR']:.1f}.",
    
        f"Write an IDF script containing a Zone, Space, SpaceList, an building surface, and its corresponding fenestration."
        f"Input specifications: Floor Area={description['FA']:.1f} square ft, Length={description['L']:.1f} ft, Width={description['W']:.1f} ft, Height={description['H']:.1f} ft, AR={description['AR']:.1f}, WWR={description['WWR']:.1f}.",
        
        f"Design an IDF file that incorporates a Zone, Space, SpaceList, a key building surface, and its fenestration for EnergyPlus simulation."
        f"Parameters: Floor Area={description['FA']:.1f} square feet, L={description['L']:.1f} ft, W={description['W']:.1f} ft, H={description['H']:.1f} ft, AR={description['AR']:.1f}, WWR={description['WWR']:.1f}.",
    
        f"Prepare an EnergyPlus IDF definition that includes a Zone, Space, SpaceList, an building surface, and an associated window or aperture."
        f"Building configuration: {description['FA']:.1f} square feet, {description['L']:.1f} ft x {description['W']:.1f} ft x {description['H']:.1f} ft, AR={description['AR']:.1f}, WWR={description['WWR']:.1f}.",
    
        f"Write an IDF file for a building with a Zone, Space, SpaceList, a building surface, and an opening fenestration for EnergyPlus analysis."
        f"Specifications: L={description['L']:.1f} ft, W={description['W']:.1f} ft, H={description['H']:.1f} ft, FA={description['FA']:.1f} sq. feet, AR={description['AR']:.1f}, WWR={description['WWR']:.1f}.",
    
        f"Develop an EnergyPlus IDF file that defines a Zone, Space, SpaceList, building surface and fenestration element, and other necessary details."
        f"Inputs: Floor Area={description['FA']:.1f} sq ft, Length={description['L']:.1f} ft, Width={description['W']:.1f} ft, Height={description['H']:.1f} ft, AR={description['AR']:.1f}, WWR={description['WWR']:.1f}.",
    
        f"Formulate an IDF snippet that includes a Zone, Space, SpaceList, building surface, and a window or glazing element."
        f"Building parameters: {description['FA']:.1f} sq ft total, Dimensions: {description['L']:.1f} ft x {description['W']:.1f} ft x {description['H']:.1f} ft, AR={description['AR']:.1f}, WWR={description['WWR']:.1f}.",

        f"How can I generate an EnergyPlus IDF file that includes a Zone, Space, SpaceList, a building surface, and a window?"
        f"My building details are: Floor Area={description['FA']:.1f} SF, Length={description['L']:.1f} ft, Width={description['W']:.1f} ft, Height={description['H']:.1f} ft, Aspect Ratio={description['AR']:.1f}, and Window-to-Wall Ratio={description['WWR']:.1f}.",
    
        f"Can you provide an IDF file containing a Zone, Space, SpaceList, building surface, and its fenestration?"
        f"The building parameters are: {description['FA']:.1f} SF total, {description['L']:.1f} ft x {description['W']:.1f} ft x {description['H']:.1f} ft, AR={description['AR']:.1f}, WWR={description['WWR']:.1f}.",
    
        f"What would an EnergyPlus IDF look like for a building with a Zone, Space, SpaceList, a building surface, and fenestration?"
        f"Here are my specifications: L={description['L']:.1f} ft, W={description['W']:.1f} ft, H={description['H']:.1f} ft, FA={description['FA']:.1f} ft2, AR={description['AR']:.1f}, WWR={description['WWR']:.1f}.",
    
        f"Can you help me create an IDF snippet for EnergyPlus that includes a Zone, Space, SpaceList, a building surface, and a glazing element?"
        f"The building details are: {description['FA']:.1f} ft², Dimensions: {description['L']:.1f} ft x {description['W']:.1f} ft x {description['H']:.1f} ft, AR={description['AR']:.1f}, WWR={description['WWR']:.1f}.",
    
        f"What is the correct IDF structure for defining a Zone, Space, SpaceList, an building surface, and a fenestration in EnergyPlus?"
        f"My building specifications are: Floor Area={description['FA']:.1f} ft², Length={description['L']:.1f} ft, Width={description['W']:.1f} ft, Height={description['H']:.1f} ft, AR={description['AR']:.1f}, WWR={description['WWR']:.1f}.",
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
