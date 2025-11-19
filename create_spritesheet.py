import os
from PIL import Image

# Configuration
assets_dir = r'c:\src\tests\dungeon-test\Assets\player'
output_file = r'c:\src\tests\dungeon-test\Assets\player_spritesheet.png'

# Map rows to files
# Row 0: IdleDown
# Row 1: WalkingDown
# Row 2: WalkingLeft
# Row 3: IdleUp
# Row 4: WalkingUp
rows = [
    ['IdleBottom1.png', 'IdleBottom2.png'],
    ['WalkingBottom1.png', 'WalkingBottom2.png'],
    ['WalkingLeft1.png', 'WalkingLeft2.png', 'WalkingLeft3.png'],
    ['IdleUp1.png', 'IdleUp2.png'],
    ['WalkingUp1.png', 'WalkingUp2.png']
]

def create_spritesheet():
    # First, determine max dimensions
    max_w = 0
    max_h = 0
    
    images = []
    
    for row_idx, file_list in enumerate(rows):
        row_imgs = []
        for filename in file_list:
            path = os.path.join(assets_dir, filename)
            if os.path.exists(path):
                img = Image.open(path)
                max_w = max(max_w, img.width)
                max_h = max(max_h, img.height)
                row_imgs.append(img)
            else:
                print(f"Warning: File not found: {path}")
                row_imgs.append(None)
        images.append(row_imgs)
    
    print(f"Cell size: {max_w}x{max_h}")
    
    # Create sheet
    # 3 columns (max frames in a row is 3), 5 rows
    sheet_w = max_w * 3
    sheet_h = max_h * 5
    
    sheet = Image.new('RGBA', (sheet_w, sheet_h), (0, 0, 0, 0))
    
    for r, row_imgs in enumerate(images):
        for c, img in enumerate(row_imgs):
            if img:
                # Center the image in the cell if it's smaller? 
                # Or just align top-left? Usually top-left or bottom-center.
                # Given these are likely same size, top-left is fine.
                # But let's center horizontally just in case.
                x = c * max_w + (max_w - img.width) // 2
                y = r * max_h + (max_h - img.height) // 2
                sheet.paste(img, (x, y))
    
    sheet.save(output_file)
    print(f"Saved spritesheet to {output_file}")

if __name__ == '__main__':
    create_spritesheet()
