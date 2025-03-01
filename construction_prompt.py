import json

# Construction Data
idf_text_construction = """
  Construction,
    Light Exterior Wall,     !- Name
    F08 Metal surface,       !- Outside Layer
    I02 50mm insulation board,  !- Layer 2
    F04 Wall air space resistance,  !- Layer 3
    G01a 19mm gypsum board;  !- Layer 4

  Construction,
    Light Roof/Ceiling,      !- Name
    M11 100mm lightweight concrete,  !- Outside Layer
    F05 Ceiling air space resistance,  !- Layer 2
    F16 Acoustic tile;       !- Layer 3

  Construction,
    Light Partitions,        !- Name
    G01a 19mm gypsum board,  !- Outside Layer
    F04 Wall air space resistance,  !- Layer 2
    G01a 19mm gypsum board;  !- Layer 3

  Construction,
    Light Floor,             !- Name
    F16 Acoustic tile,       !- Outside Layer
    F05 Ceiling air space resistance,  !- Layer 2
    M11 100mm lightweight concrete;  !- Layer 3

  Construction,
    Light Furnishings,       !- Name
    G05 25mm wood;           !- Outside Layer

  Construction,
    Medium Exterior Wall,    !- Name
    M01 100mm brick,         !- Outside Layer
    I02 50mm insulation board,  !- Layer 2
    F04 Wall air space resistance,  !- Layer 3
    G01a 19mm gypsum board;  !- Layer 4

  Construction,
    Medium Roof/Ceiling,     !- Name
    M14a 100mm heavyweight concrete,  !- Outside Layer
    F05 Ceiling air space resistance,  !- Layer 2
    F16 Acoustic tile;       !- Layer 3

  Construction,
    Medium Partitions,       !- Name
    G01a 19mm gypsum board,  !- Layer 1
    F04 Wall air space resistance,  !- Layer 2
    G01a 19mm gypsum board;  !- Layer 3

  Construction,
    Medium Floor,            !- Name
    F16 Acoustic tile,       !- Outside Layer
    F05 Ceiling air space resistance,  !- Layer 2
    M14a 100mm heavyweight concrete;  !- Layer 3

  Construction,
    Medium Furnishings,      !- Name
    G05 25mm wood;           !- Outside Layer

  Construction,
    Heavy Exterior Wall,     !- Name
    M01 100mm brick,         !- Outside Layer
    M15 200mm heavyweight concrete,  !- Layer 2
    I02 50mm insulation board,  !- Layer 3
    F04 Wall air space resistance,  !- Layer 4
    G01a 19mm gypsum board;  !- Layer 5

  Construction,
    Heavy Roof/Ceiling,      !- Name
    M15 200mm heavyweight concrete,  !- Outside Layer
    F05 Ceiling air space resistance,  !- Layer 2
    F16 Acoustic tile;       !- Layer 3

  Construction,
    Heavy Partitions,        !- Name
    G01a 19mm gypsum board,  !- Outside Layer
    M05 200mm concrete block,!- Layer 2
    G01a 19mm gypsum board;  !- Layer 3

  Construction,
    Heavy Floor,             !- Name
    F16 Acoustic tile,       !-Layer 1
    F05 Ceiling air space resistance,  !- Layer 2
    M15 200mm heavyweight concrete;  !- Layer 3

  Construction,
    Ext wall,          !- Name
    brick,         !- Layer 1
    concrete,  !- Layer 2
    insulation board,  !- Layer 3
    air space resistance,  !- Layer 4
    gypsum board;  !- Layer 5

  Construction,
    Heavy Ceiling,      !- Name
    M15 concrete,  !- Outside Layer
    F05 air space resistance,  !- Layer 2
    Acoustic tile;       !- Layer 3

  Construction,
    Partitions,        !- Name
    gypsum board,  !- Outside Layer
    concrete block,!- Layer 2
    gypsum board;  !- Layer 3

  Construction,
    floor const,             !- Name
    Acoustic tile,       !- Outside Layer
    concrete;  !- Layer 2


"""


# Split into blocks for each Construction entry
construction_blocks = [block.strip() for block in idf_text_construction.split("Construction,") if block.strip()]

# Parse each block to create prompts
construction_datasets = []

for block in construction_blocks:
    lines = block.split("\n")
    name = lines[0].split(",")[0].strip()  # Extract construction name
    layers = [line.split(",")[0].strip() for line in lines[1:] if line.strip()]  # Extract layers
    layers_with_comments = [line.strip() for line in lines[1:] if line.strip()]  # Layers with comments

    # Create the user prompt without the comments (Layer X)
    layer_text = ", ".join(layers)

    # Create the answer with layers including the comments
    layers_with_comments_text = ", ".join(layers_with_comments)

    # Format the answer properly to match the required structure
    answer_text = f"Construction,{name},{layers_with_comments_text};"

    # Create the final dataset entry
    construction_datasets.append({
        "user": f"Create a construction called '{name}' with the following layers: {layer_text}.",
        "answer": answer_text
    })

# Save dataset to JSON file
with open("construction_datasets.json", "w") as f:
    json.dump(construction_datasets, f, indent=2)

# Print output for verification
print(json.dumps(construction_datasets, indent=2))