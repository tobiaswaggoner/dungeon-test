import json
import re

analysis_file = "tile_analysis.json"
output_file = "tileset_index.json"

def get_visual_description(tile_id, data):
    avg_color = data["avg_color"]
    avg_alpha = data["avg_alpha"]
    complexity = data["complexity"]
    
    r, g, b = avg_color
    brightness = (r + g + b) / 3
    
    # Color detection
    is_grey = abs(r - g) < 10 and abs(g - b) < 10
    is_brown = r > g and g > b and r > 40
    is_red = r > g + 20 and r > b + 20
    is_blue = b > r + 20 and b > g + 20
    is_green = g > r + 20 and g > b + 20
    
    # Texture detection
    texture = "Smooth" if complexity < 10 else "Textured" if complexity < 25 else "Rough"
    
    # Base material
    material = "Unknown"
    if is_grey:
        material = "Stone"
    elif is_brown:
        material = "Wood"
    elif is_red:
        material = "Red Brick/Carpet"
    elif is_blue:
        material = "Water/Ice"
    elif is_green:
        material = "Grass/Moss"
        
    # Brightness modifier
    shade = "Dark" if brightness < 60 else "Medium" if brightness < 100 else "Light"
    
    # Construct description
    desc = f"{shade} {texture} {material}"
    
    # Refinements based on common RPG tileset patterns (Rows often share themes)
    match = re.match(r"([A-Z]+)(\d+)", tile_id)
    if match:
        row_char = match.group(1) # Column actually (A, B, C...)
        col_num = int(match.group(2)) # Row actually (1, 2, 3...)
        
        # Heuristics based on typical tileset layouts
        # Row 1 (1): Often top walls
        if col_num == 1:
            if material == "Stone": desc = f"{shade} Stone Wall Top"
            if material == "Wood": desc = f"{shade} Wooden Wall Top"
            
        # Row 2 (2): Often floors
        if col_num == 2:
            if material == "Stone": desc = f"{shade} Stone Floor"
            if material == "Wood": desc = f"{shade} Wooden Floor"
            
        # Row 3 (3): Often bottom walls or variations
        if col_num == 3:
            desc += " (Lower Wall/Variation)"
            
        # Row 6 (6): Often props or secondary theme
        if col_num == 6:
            desc += " (Prop/Object)"

    return desc

def main():
    with open(analysis_file, 'r') as f:
        analysis = json.load(f)
        
    index = {}
    
    # Sort keys naturally
    sorted_keys = sorted(analysis.keys(), key=lambda k: (re.match(r"([A-Z]+)", k).group(1), int(re.match(r"[A-Z]+(\d+)", k).group(1))))
    
    for tile_id in sorted_keys:
        if tile_id in analysis:
            index[tile_id] = get_visual_description(tile_id, analysis[tile_id])
        else:
            index[tile_id] = "Unknown Tile"
            
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=4, ensure_ascii=False)
        
    print(f"Generated {output_file}")

if __name__ == "__main__":
    main()
