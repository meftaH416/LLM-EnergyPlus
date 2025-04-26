import random
import json

random.seed(42)

def generate_example(example_type=None, forced_surface_type=None):
    linear_units = ["m", "meter"]
    area_units = ["sq.m", "square meter", "m2", "m^2"]
    percent_decalartion = ['%', 'percent', 'percentile']
    surface_types = ['wall', 'floor', 'roof']

    fraction_phrases = [
        "percent of the total area", "as a percentage of the surface", "portion of the surface", "percentage of the {surface_type}"
    ]
    geometry_phrases = [
        "coordinates for", "points for", "position of vertices for", "list vertices of"
    ]

    if example_type is None:
        example_type = random.choice(["fraction", "geometry"])

    if example_type == "fraction":
        width = random.randint(2, 30)
        height = random.randint(2, 4)
        fraction = random.randint(10, 90)
        percent_dec = random.choice(percent_decalartion)
        area = width * height
        window_area = (fraction / 100) * area

        area_unit = random.choice(area_units)
        linear_unit = random.choice(linear_units)

        if forced_surface_type:
            surface_type = forced_surface_type
        else:
            surface_type = random.choice(surface_types)

        fraction_phrase = random.choice(fraction_phrases).replace("{surface_type}", surface_type)

        user = f"What is {fraction} {percent_dec} of a {surface_type} area that is {width} {linear_unit} wide and {height} {linear_unit} high?"
        assistant = f"{surface_type.capitalize()} area = {width} * {height} = {area} {area_unit}. {fraction}% {fraction_phrase} is {area} * {fraction}% = {window_area} {area_unit}."

    elif example_type == "geometry":
        length = random.randint(2, 30)
        width = random.randint(2, 30)
        height = random.randint(2, 4)
        start_x = random.randint(0, 5)
        start_y = random.randint(0, 5)

        if forced_surface_type:
            surface_type = forced_surface_type
        else:
            surface_type = random.choice(surface_types)

        unit = random.choice(linear_units)
        geometry_phrase = random.choice(geometry_phrases)

        if surface_type == "wall":
            user = f"Generate {geometry_phrase} a vertical {surface_type} {length} {unit} wide and {height} {unit} tall, starting at ({start_x},{start_y},0)."
            assistant = (
                f"Bottom left: ({start_x},{start_y},0),"
                f"Bottom right: ({start_x + length},{start_y},0),"
                f"Top right: ({start_x + length},{start_y},{height}),"
                f"Top left: ({start_x},{start_y},{height})."
            )

        elif surface_type == "floor":
            user = f"List {geometry_phrase} a {surface_type} that is {length} {unit} long and {width} {unit} wide at ground level."
            assistant = (
                f"Floor points: (0,0,0), ({length},0,0), ({length},{width},0), (0,{width},0)."
            )

        elif surface_type == "roof":
            user = f"Generate {geometry_phrase} a flat {surface_type} that is {length} {unit} long and {width} {unit} wide at elevation {height} {unit}."
            assistant = (
                f"Roof points: (0,0,{height}), ({length},0,{height}), ({length},{width},{height}), (0,{width},{height})."
            )

    return {"user": user, "assistant": assistant}

# Generate dataset
def generate_dataset(n):
    dataset = []

    # Ensure at least one of each surface
    surfaces = ['wall', 'floor', 'roof']
    for surface in surfaces:
        dataset.append(generate_example(example_type="geometry", forced_surface_type=surface))
        dataset.append(generate_example(example_type="fraction", forced_surface_type=surface))

    remaining = n - 2 * len(surfaces)
    for _ in range(remaining):
        dataset.append(generate_example())

    random.shuffle(dataset)
    return dataset

# Set dataset size
n = 1000
dataset = generate_dataset(n)

# Save dataset
with open("geometry_fraction_dataset.json", "w") as f:
    for example in dataset:
        f.write(json.dumps(example) + "\n")

print(f"Dataset of {n} examples saved as 'geometry_fraction_dataset.json'")
