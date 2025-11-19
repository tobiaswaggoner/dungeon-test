import os
import json
import re

# Configuration
tiles_dir = "Individual_Tiles"
output_file = "tileset_index.json"

# Known descriptions from dungeon.html analysis
# Format: "ID": "Description"
known_descriptions = {
    "A1": "Wall Top / Default Wall (Common)",
    "B1": "Wall Variant 1 (Common)",
    "C1": "Wall Variant 2 (Common)",
    "D1": "Wall Variant 3 (Less Common)",
    "I1": "Door Vertical",
    "N1": "Door Horizontal",
    
    "A2": "Floor / Default Floor (Very Common)",
    "B2": "Floor Variant 1 (Common)",
    "C2": "Floor Variant 2 (Less Common)",
    
    "C12": "Floor Rare Variant",
    "D12": "Wall Rare Variant",
    "S12": "Treasure Room Floor",
    "H13": "Combat Room Floor",
    "T9": "Floor Special Rare"
}

def generate_index():
    index = {}
    
    # Get all png files
    files = [f for f in os.listdir(tiles_dir) if f.endswith('.png')]
    
    # Sort files naturally (A1, A2, ... B1...)
    # But actually user might prefer A1, B1, C1... (Row by Row) or A1, A2... (Col by Col)
    # The filenames are A1.png.
    # Let's just populate the dictionary.
    
    for filename in files:
        tile_id = os.path.splitext(filename)[0]
        
        # Determine description
        description = known_descriptions.get(tile_id, f"Tile {tile_id}")
        
        # Try to infer type from row/col if possible
        # Parse ID: Letter(s) + Number
        match = re.match(r"([A-Z]+)(\d+)", tile_id)
        if match:
            col_str, row_str = match.groups()
            col_idx = 0
            for char in col_str:
                col_idx = col_idx * 26 + (ord(char) - ord('A'))
            
            row_idx = int(row_str) - 1 # 0-indexed row
            
            # Heuristics based on known types
            # Row 0 (1): Walls/Doors
            # Row 1 (2): Floors
            
            if description == f"Tile {tile_id}":
                if row_idx == 0:
                    description += " (Likely Wall/Structure)"
                elif row_idx == 1:
                    description += " (Likely Floor)"
        
        index[tile_id] = description

    # Sort keys for the output JSON
    sorted_keys = sorted(index.keys(), key=lambda k: (re.match(r"([A-Z]+)", k).group(1), int(re.match(r"[A-Z]+(\d+)", k).group(1))))
    
    sorted_index = {k: index[k] for k in sorted_keys}
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(sorted_index, f, indent=4, ensure_ascii=False)
    
    print(f"Generated {output_file} with {len(index)} entries.")

if __name__ == "__main__":
    generate_index()
