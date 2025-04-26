import random
import json

# Function to generate random geometric and fraction math examples
def generate_example():
    units = ["m", "meter", "sq.m", "m²", "square meter", "m^2"]
    fraction_phrases = [
        "percent", "of the total area", "as a percentage", "of the surface", "percentage of the wall"
    ]
    geometry_phrases = [
        "coordinates for", "points for", "position of", "locations of", "vertices for"
    ]
    example_type = random.choice(["fraction", "geometry"])

    if example_type == "fraction":
        # Random values for fractions and math
        width = random.randint(5, 15)  # Wall width in meters
        height = random.randint(2, 6)  # Wall height in meters
        fraction = random.randint(30, 70)  # Random fraction between 30-70%
        
        area = width * height
        window_area = (fraction / 100) * area

        # Random unit variations for fraction
        unit = random.choice(units)
        fraction_phrase = random.choice(fraction_phrases)

        # Random prompt and response for fraction
        prompt = f"What is {fraction}% of a wall area that is {width} {unit} wide and {height} {unit} high?"
        response = f"Wall area = {width} × {height} = {area} {unit}². {fraction}% {fraction_phrase} {area} = {window_area} {unit}²."

    elif example_type == "geometry":
        # Random values for geometry
        length = random.randint(4, 10)  # Length in meters
        width = random.randint(4, 10)   # Width in meters
        height = random.randint(3, 6)   # Height in meters
        start_x = random.randint(0, 5)
        start_y = random.randint(0, 5)
        
        # Random surface type
        surface_type = random.choice(["wall", "floor", "roof"])
        
        # Random unit variations for geometry
        unit = random.choice(units)
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
with open("geometry_fraction_dataset.jsonl", "w") as f:
    for example in dataset:
        f.write(json.dumps(example) + "\n")

print(f"Dataset of {n} examples saved as 'geometry_fraction_dataset.jsonl'")
