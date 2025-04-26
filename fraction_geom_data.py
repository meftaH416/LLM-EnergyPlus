import random
import json

# Function to generate random geometric and fraction math examples
def generate_example():
    # Units for length (geometry)
    linear_units = ["m", "meter"]
    
    # Units for area (fraction)
    area_units = ["sq.m", "m²", "square meter", "m2", "m^2"]

    fraction_phrases = [
        "percent", "of the total area", "as a percentage", "of the surface", "percentage of the wall"
    ]
    geometry_phrases = [
        "coordinates for", "points for", "position of", "locations of", "vertices for"
    ]
    example_type = random.choice(["fraction", "geometry"])

    if example_type == "fraction":
        # Random values for fractions and math
        width = random.randint(2, 30)  # Wall width in meters (linear unit)
        height = random.randint(2, 4)  # Wall height in meters (linear unit)
        fraction = random.randint(10, 90)  # Random fraction between 10-90%
        
        area = width * height  # Calculating area in m²
        window_area = (fraction / 100) * area

        # Random unit variations for fraction (area units only)
        area_unit = random.choice(area_units)  # Only area-related units for this case
        fraction_phrase = random.choice(fraction_phrases)

        # Random prompt and response for fraction
        prompt = f"What is {fraction}% of a wall area that is {width} {random.choice(linear_units)} wide and {height} {random.choice(linear_units)} high?"
        response = f"Wall area = {width} × {height} = {area} {area_unit}. {fraction}% {fraction_phrase} {area} = {window_area} {area_unit}."

    elif example_type == "geometry":
        # Random values for geometry (linear units only)
        length = random.randint(4, 10)  # Length in meters
        width = random.randint(4, 10)   # Width in meters
        height = random.randint(3, 6)   # Height in meters
        start_x = random.randint(0, 5)
        start_y = random.randint(0, 5)
        
        # Random surface type
        surface_type = random.choice(["wall", "floor", "roof"])
        
        # Random unit variations for geometry (linear units only)
        unit = random.choice(linear_units)  # Only linear units for this case (m or meter)
        geometry_phrase = random.choice(geometry_phrases)

        if surface_type == "wall":
            prompt = f"Generate {geometry_phrase} a vertical {surface_type} {length} {unit} wide, {height} {unit} tall, starting at ({start_x},{start_y},0)."
            response = f"Bottom left: ({start_x},{start_y},0)\nBottom right: ({start_x + length},{start_y},0)\nTop right: ({start_x + length},{start_y},{height})\nTop left: ({start_x},{start_y},{height})."
        
        elif surface_type == "floor":
            prompt = f"List the {geometry_phrase} a {surface_type} surface {length} {unit} long, {width} {unit} wide."
            response = f"Floor points: (0,0,0), ({length},0,0), ({length},{width},0), (0,{width},0)."
        
        elif surface_type == "roof":
            prompt = f"Generate {geometry_phrase} a sloped {surface_type} {length} {unit} long, {width} {unit} wide, starting at ({start_x},{start_y},0)."
            response = f"Bottom left: ({start_x},{start_y},0)\nBottom right: ({start_x + length},{start_y},0)\nTop right: ({start_x + length},{start_y},{height})\nTop left: ({start_x},{start_y},{height})."

    # Return the example as a dictionary
    return {"prompt": prompt, "response": response}

# Generate dataset of size n
def generate_dataset(n):
    dataset = []
    for _ in range(n):
        dataset.append(generate_example())
    return dataset

# Generate 1000 examples
n = 1000
dataset = generate_dataset(n)

# Save dataset to JSONL file
with open("geometry_fraction_dataset_randomized.jsonl", "w") as f:
    for example in dataset:
        f.write(json.dumps(example) + "\n")

print(f"Dataset of {n} examples saved as 'geometry_fraction_dataset_randomized.jsonl'")
