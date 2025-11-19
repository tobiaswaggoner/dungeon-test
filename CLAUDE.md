# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a browser-based procedural dungeon generator with real-time player movement, built entirely in vanilla JavaScript within a single HTML file. The game features:
- BSP (Binary Space Partitioning) dungeon generation algorithm
- Player character with 4-directional movement and animation
- Fog of war system that reveals rooms as the player explores
- Collision detection against walls
- Room-based dungeon layout with doors connecting rooms
- Different room types (empty, treasure, combat)

## Architecture

### Single-File Application
The entire game is contained in `dungeon.html` - a single HTML file with embedded JavaScript and CSS. There is no build process, bundler, or framework. Simply open the file in a browser to run.

### Core Systems

**Dungeon Generation (BSP-based)**
- Uses Binary Space Partitioning to recursively divide space into rooms
- `BSPNode` class handles the tree structure and recursive splitting (dungeon.html:494-615)
- `generateRooms()` creates the BSP tree and fills it with floor tiles (dungeon.html:617-640)
- `connectRooms()` uses Union-Find algorithm to ensure all rooms are reachable (dungeon.html:667-754)
- Room types are randomly assigned: 60% empty, 20% treasure, 10% combat (dungeon.html:566-574)

**Rendering System**
- Canvas-based rendering with camera system centered on player (dungeon.html:825-938)
- Tileset-based graphics using 64x64 tiles from `Assets/Castle-Dungeon2_Tiles/Tileset.png`
- Weighted random tile variant selection for visual variety (dungeon.html:142-180)
- Tile variants are pre-generated and stored in `tileVariants` array to maintain consistency
- Fog of war implemented by checking room visibility before rendering (dungeon.html:873-902)

**Player System**
- Player sprite is a 3-column x 5-row spritesheet (`Assets/player_spritesheet.png`)
- Spritesheet layout: Row 0=IdleDown, Row 1=WalkDown, Row 2=WalkLeft (flipped for right), Row 3=IdleUp, Row 4=WalkUp
- Movement uses WASD or arrow keys at 6 tiles/second (dungeon.html:251-330)
- Collision detection checks corners of player bounding box (dungeon.html:332-365)
- Animation system with frame-based sprite rendering (dungeon.html:385-433)

**Fog of War**
- Each room has a `visible` property tracked in the `rooms` array
- `roomMap` is a 2D array mapping each tile to its room index (-1 for walls, -2 for doors)
- Player position updates fog of war by revealing the current room (dungeon.html:367-378)
- Walls/doors are visible if any adjacent room is visible (dungeon.html:878-895)

**Data Structures**
- `dungeon`: 2D array storing tile types (EMPTY=0, FLOOR=1, WALL=2, DOOR=3, CORNER=4)
- `rooms`: Array of room objects with properties: id, x, y, width, height, visible, neighbors, type
- `roomMap`: 2D array mapping grid positions to room IDs
- `tileVariants`: 2D array of pre-selected tile variants for consistent rendering

## Development Workflow

### Running the Game
```bash
# Simply open the HTML file in a browser (no build process)
start dungeon.html  # Windows
open dungeon.html   # macOS
xdg-open dungeon.html  # Linux
```

Or use a local server:
```bash
python -m http.server 8000
# Then navigate to http://localhost:8000/dungeon.html
```

### Asset Management

**Player Spritesheet Generation**
The player spritesheet is generated from individual PNG files using a Python script:
```bash
python create_spritesheet.py
```
This creates `Assets/player_spritesheet.png` from individual frames in `Assets/player/`.

**Tileset**
The dungeon tileset is at `Assets/Castle-Dungeon2_Tiles/Tileset.png` (64x64 tiles).
- `tileset_index.json` contains a mapping of grid positions to tile descriptions
- Several Python scripts exist for analyzing and indexing tiles (analyze_tiles.py, generate_index.py, etc.)

### Key Configuration Constants

Located at the top of the script in dungeon.html:
- `DUNGEON_WIDTH/HEIGHT`: Size of dungeon grid (100x100)
- `MIN_ROOM_SIZE/MAX_ROOM_SIZE`: BSP splitting constraints (5-10 tiles)
- `PLAYER_SPEED_TILES`: Movement speed (6 tiles/second)
- `TILE_SOURCE_SIZE`: Source tile size in tileset (64px)
- `WALL_VARIANTS/FLOOR_VARIANTS`: Arrays of tile coordinates with weighted probabilities

### Important Implementation Details

**Tile Coordinate System**
- Tiles are referenced by {x, y} coordinates in the tileset grid
- Example: `{x: 0, y: 1}` means column 0, row 1 in the 64x64 tile grid
- `getTileCoords()` function maps tile types to tileset coordinates (dungeon.html:769-823)

**Collision System**
- Uses a reduced player size (0.5 of tile size) for more forgiving collision (dungeon.html:96)
- Checks all 4 corners of player bounding box against tile types
- Walls and empty tiles are solid; floors and doors are passable
- Doors convert to floor tiles when player walks through them (dungeon.html:313-321)

**Union-Find for Room Connectivity**
- Ensures all rooms are reachable by creating a minimal spanning tree of connections
- Scans for possible door positions where rooms are adjacent (dungeon.html:672-710)
- Connections are shuffled for randomness, then added until all rooms are connected
- Optional extra doors (2% chance) create loops in the dungeon (dungeon.html:733-747)

### Common Modifications

**Changing Dungeon Size**
Modify `DUNGEON_WIDTH` and `DUNGEON_HEIGHT` constants (dungeon.html:71-72).

**Adjusting Room Types**
The room type distribution is controlled in the BSPNode.fillRooms() method (dungeon.html:566-574).

**Modifying Tile Appearance**
- For floor tiles: Adjust `FLOOR_VARIANTS` array with different tileset coordinates and weights (dungeon.html:151-157)
- For wall tiles: Adjust `WALL_VARIANTS` array (dungeon.html:143-149)
- Room-specific tiles are set in `getTileCoords()` based on room type (dungeon.html:776-789)

**Player Animation**
Player sprite layout is in `create_spritesheet.py` (rows array, lines 14-20). Modify to change animation frames.

## Technical Constraints

- No external dependencies - pure vanilla JavaScript
- All code must remain in dungeon.html for simplicity
- Assets must be in the Assets/ directory structure
- Canvas rendering only (no WebGL)
- Tileset tiles must be 64x64 pixels
- Player spritesheet follows specific 3x5 grid layout
