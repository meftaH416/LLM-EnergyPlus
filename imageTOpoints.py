import os
import json
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from tqdm import tqdm

# CONFIG
num_samples = 500
img_size = 256
shape_types = ['square', 'rectangle', 'l_shape', 'cross', 'plus']
output_dir = 'floorplan_dataset'
os.makedirs(os.path.join(output_dir, 'images'), exist_ok=True)
jsonl_path = os.path.join(output_dir, 'annotations.jsonl')

# SHAPE FUNCTIONS - ANCHORED AT (0, 0)
def square():
    s = random.uniform(3, 7)
    pts = [(0, 0), (s, 0), (s, s), (0, s)]
    return pts

def rectangle():
    w = random.uniform(4, 8)
    h = random.uniform(2, 5)
    pts = [(0, 0), (w, 0), (w, h), (0, h)]
    return pts

def l_shape():
    w = random.uniform(3, 5)
    h = random.uniform(3, 5)
    t = random.uniform(1, 2)
    pts = [
        (0, 0),
        (w, 0),
        (w, t),
        (t, t),
        (t, h),
        (0, h)
    ]
    return pts

def cross():
    arm = random.uniform(2, 4)
    thick = random.uniform(0.5, 1.0)
    c = arm + thick

    pts = [
        (c, 0), (c+thick, 0),
        (c+thick, c), (2*c+thick, c),
        (2*c+thick, c+thick), (c+thick, c+thick),
        (c+thick, 2*c+thick), (c, 2*c+thick),
        (c, c+thick), (0, c+thick),
        (0, c), (c, c)
    ]

    # Normalize to bottom-left = (0, 0)
    min_x = min(p[0] for p in pts)
    min_y = min(p[1] for p in pts)
    return [(x - min_x, y - min_y) for x, y in pts]

def plus():
    size = random.uniform(2, 4)
    thick = random.uniform(0.5, 1.0)
    c = size

    pts = [
        (c - thick, 0), (c + thick, 0),
        (c + thick, c - thick), (2*c, c - thick),
        (2*c, c + thick), (c + thick, c + thick),
        (c + thick, 2*c), (c - thick, 2*c),
        (c - thick, c + thick), (0, c + thick),
        (0, c - thick), (c - thick, c - thick)
    ]

    # Normalize to bottom-left = (0, 0)
    min_x = min(p[0] for p in pts)
    min_y = min(p[1] for p in pts)
    return [(x - min_x, y - min_y) for x, y in pts]

shape_generators = {
    'square': square,
    'rectangle': rectangle,
    'l_shape': l_shape,
    'cross': cross,
    'plus': plus
}

# MAIN LOOP
with open(jsonl_path, 'w') as f:
    for i in tqdm(range(num_samples)):
        shape_name = random.choice(shape_types)
        pts_2d = shape_generators[shape_name]()
        pts_3d = [(round(x, 2), round(y, 2), 0.0) for x, y in pts_2d]

        # Plot shape
        fig, ax = plt.subplots(figsize=(2.56, 2.56), dpi=100)
        ax.set_xlim(0, 15)
        ax.set_ylim(0, 15)
        ax.set_aspect('equal')
        ax.axis('off')

        polygon = patches.Polygon(pts_2d, closed=True, fill=False, edgecolor='black', linewidth=2)
        ax.add_patch(polygon)

        # Save image
        img_path = os.path.join(output_dir, 'images', f'{i:04d}.png')
        plt.savefig(img_path, bbox_inches='tight', pad_inches=0)
        plt.close()

        # Save annotation
        f.write(json.dumps({
            'image': f'images/{i:04d}.png',
            'text': str(pts_3d),
            'shape': shape_name
        }) + '\n')
