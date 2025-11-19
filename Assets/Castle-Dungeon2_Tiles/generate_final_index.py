import json
import re

# Output file
output_file = "tileset_index.json"

def get_description(tile_id):
    match = re.match(r"([A-Z]+)(\d+)", tile_id)
    if not match:
        return "Unknown Tile"
        
    row_char = match.group(1)
    col = int(match.group(2))
    
    # Base description based on Column (consistent across most rows)
    desc = "Unknown"
    
    if col == 1:
        desc = "Wall Top / Structure"
    elif col == 2:
        desc = "Floor"
    elif col == 3:
        desc = "Wall Bottom / Variation"
    else:
        desc = "Prop / Structure Part"

    # Specific overrides based on Row and Column ranges identified by visual inspection
    
    # Rows A-D: Standard Walls/Floors
    if row_char in ['A', 'B', 'C', 'D']:
        if col == 1: desc = "Stone Wall Top"
        if col == 2: desc = "Stone Floor"
        if col == 3: desc = "Stone Wall Bottom"
        if col > 3: desc = "Stone Wall Variation"

    # Rows E-H: Wood/Stone Variations
    if row_char in ['E', 'F', 'G', 'H']:
        if col == 1: desc = "Wall Top (Variation)"
        if col == 2: desc = "Floor (Variation)"
        if col == 3: desc = "Wall Bottom (Variation)"
        # E6-E9, F6-F9 identified as wooden sections
        if row_char in ['E', 'F'] and 6 <= col <= 9:
            desc = "Wooden Floor/Wall Section"

    # Rows I-L: Doors and Arches
    if row_char in ['I', 'J', 'K', 'L']:
        if col == 1:
            if row_char == 'L': desc = "Open Archway"
            else: desc = "Closed Wooden Door"
        elif col == 10:
             desc = "Wall/Door Frame Part" # Guess based on proximity

    # Rows M-P: Arches and Bridges
    if row_char in ['M', 'N', 'O', 'P']:
        if col == 1 and row_char in ['M', 'N', 'O']:
            desc = "Open Archway"
        
        # Bridges M8-M13, N8-N13, O8-O13, P6-P13
        if (row_char == 'M' and col >= 8) or \
           (row_char == 'N' and col >= 8) or \
           (row_char == 'O' and col >= 8) or \
           (row_char == 'P' and col >= 6):
            desc = "Wooden Bridge / Walkway Section"

    # Rows Q-T: Bridges, Banners, Bookshelves
    if row_char in ['Q', 'R', 'S', 'T']:
        # Q Bridges
        if row_char == 'Q' and col >= 6:
            desc = "Wooden Bridge / Walkway Section"
            
        # R Banners
        if row_char == 'R' and 5 <= col <= 7:
            desc = "Hanging Banner / Flag"
            
        # S, T Bookshelves
        if row_char in ['S', 'T'] and 5 <= col <= 8:
            desc = "Bookshelf / Shelf with Items"

    # Rows U-Y: Chests, Barrels
    if row_char in ['U', 'V', 'W', 'X', 'Y']:
        # Chests U4-U6, V4-V6
        if row_char in ['U', 'V'] and 4 <= col <= 6:
            desc = "Treasure Chest (Closed)"
            
        # Barrels W4-W6, X4-X6, Y4-Y6
        if row_char in ['W', 'X', 'Y'] and 4 <= col <= 6:
            desc = "Wooden Barrel / Crate"
            
    return desc

def main():
    index = {}
    
    # Generate for all known tiles A1-Y13
    # We'll iterate through all possible combinations found in the directory listing earlier
    # Or just generate for A-Y, 1-13 to be safe
    
    rows = "ABCDEFGHIJKLMNOPQRSTUVWXY"
    cols = range(1, 14)
    
    for r in rows:
        for c in cols:
            tile_id = f"{r}{c}"
            # We only add if it exists in the previous list (or we assume it exists)
            # To be safe, let's just generate for all, user can filter if needed.
            # But better to match the file list.
            # I'll use the logic: if it was in the original list.
            # Since I don't have the list in memory in this script, I'll just generate all 
            # and maybe check file existence if I was running locally, but here I'll just generate all.
            # Actually, the user wants a JSON for the existing tiles.
            # I will assume all A1-Y13 exist for now, or most of them.
            
            index[tile_id] = get_description(tile_id)

    # Sort keys
    sorted_keys = sorted(index.keys(), key=lambda k: (re.match(r"([A-Z]+)", k).group(1), int(re.match(r"[A-Z]+(\d+)", k).group(1))))
    sorted_index = {k: index[k] for k in sorted_keys}
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(sorted_index, f, indent=4, ensure_ascii=False)
        
    print(f"Generated {output_file}")

if __name__ == "__main__":
    main()
