import json
import re

analysis_file = "tile_analysis.json"
output_file = "tileset_index.json"

def get_description(tile_id, data):
    avg_color = data["avg_color"]
    avg_alpha = data["avg_alpha"]
    complexity = data["complexity"]
    
    r, g, b = avg_color
    
    # Basic color classification
    is_grey = abs(r - g) < 5 and abs(g - b) < 5
    is_brown = r > g and g > b and r > 50
    is_dark = (r + g + b) / 3 < 60
    is_light = (r + g + b) / 3 > 100
    
    # Determine type based on properties
    if avg_alpha < 250:
        return "Prop / Decoration (Transparent)"
        
    if is_grey:
        if is_dark:
            if complexity < 10:
                return "Solid Dark Wall / Void"
            else:
                return "Dark Stone Wall"
        elif is_light:
            if complexity < 15:
                return "Clean Stone Floor"
            else:
                return "Textured Stone Floor"
        else:
            return "Stone Wall / Floor"
            
    if is_brown:
        if complexity > 20:
            return "Wooden Floor / Structure"
        else:
            return "Wood / Dirt"
            
    # Fallback based on row heuristics if color is ambiguous
    # A-D: Walls/Floors
    # E-H: Variations
    # I-L: Doors/Windows?
    
    return f"Tile {tile_id} (Color: {r},{g},{b})"

def main():
    with open(analysis_file, 'r') as f:
        analysis = json.load(f)
        
    index = {}
    
    # Sort keys to process in order
    sorted_keys = sorted(analysis.keys(), key=lambda k: (re.match(r"([A-Z]+)", k).group(1), int(re.match(r"[A-Z]+(\d+)", k).group(1))))
    
    for tile_id in sorted_keys:
        data = analysis[tile_id]
        desc = get_description(tile_id, data)
        
        # Refine description based on Row/Col position
        match = re.match(r"([A-Z]+)(\d+)", tile_id)
        if match:
            row_char = match.group(1)
            col_idx = int(match.group(2))
            
            # Specific overrides based on common tileset patterns
            # and the "visual" data we have
            
            # Walls often have similar colors in a row
            if row_char in ['A', 'B', 'C', 'D'] and col_idx == 1:
                 desc = desc.replace("Stone Wall / Floor", "Wall Top")
            
            # Floors often in column 2
            if col_idx == 2:
                desc = desc.replace("Stone Wall / Floor", "Floor Tile")
                
            # Doors often have specific colors (brown/wood)
            if "Wood" in desc and (row_char in ['I', 'N']):
                desc = "Door / Wooden Object"
                
        index[tile_id] = desc
        
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=4, ensure_ascii=False)
        
    print(f"Generated {output_file}")

if __name__ == "__main__":
    main()
