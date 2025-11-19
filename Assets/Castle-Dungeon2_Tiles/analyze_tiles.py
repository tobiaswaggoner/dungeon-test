import os
import json
from PIL import Image
import statistics

tiles_dir = "Individual_Tiles"
output_file = "tile_analysis.json"

def analyze_tile(path):
    try:
        img = Image.open(path).convert('RGBA')
        width, height = img.size
        pixels = list(img.getdata())
        
        r_vals = [p[0] for p in pixels]
        g_vals = [p[1] for p in pixels]
        b_vals = [p[2] for p in pixels]
        a_vals = [p[3] for p in pixels]
        
        avg_r = statistics.mean(r_vals)
        avg_g = statistics.mean(g_vals)
        avg_b = statistics.mean(b_vals)
        avg_a = statistics.mean(a_vals)
        
        # Simple complexity metric: standard deviation of brightness
        brightness = [(r+g+b)/3 for r,g,b in zip(r_vals, g_vals, b_vals)]
        complexity = statistics.stdev(brightness) if len(brightness) > 1 else 0
        
        return {
            "avg_color": (int(avg_r), int(avg_g), int(avg_b)),
            "avg_alpha": int(avg_a),
            "complexity": int(complexity),
            "size": (width, height)
        }
    except Exception as e:
        return {"error": str(e)}

def main():
    results = {}
    files = sorted([f for f in os.listdir(tiles_dir) if f.endswith('.png')])
    
    for f in files:
        path = os.path.join(tiles_dir, f)
        results[f.replace('.png', '')] = analyze_tile(path)
        
    # Group by similarity for easier reading
    # We'll just dump the raw data first
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
        
    print(f"Analyzed {len(results)} tiles.")

if __name__ == "__main__":
    main()
