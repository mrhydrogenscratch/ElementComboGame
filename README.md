# Element Combo Game

A Little Alchemy-style element combination game built with PyGame. Start with 4 base elements (earth, fire, water, air) and combine them via drag-and-drop to discover 200 total elements across 7 tiers.

## Setup

1. Install dependencies:
   ```bash
   pip3 install pygame
   ```.

2. Run the game:
   ```bash
   python3 game.py
   ```

Requires Python 3.10+.

## Controls

- **Drag & drop** one element onto another to combine
- **Right-click** an element to remove it from the canvas
- **Sidebar** — click any discovered element to spawn it
- **Text input** — type an element name + Enter to spawn, Tab to autocomplete

## Buttons

| Button | Action |
|--------|--------|
| Light/Dark | Toggle theme |
| Sweep | Clear the board |
| Clear | Reset game to 4 base elements (requires confirmation) |
| Saves | Open save file manager |
| Hint | Get a hint (60s cooldown) |

## Features

- 100 elements, 105+ recipes
- 9 element categories with colour-coded chips
- Star ratings showing element tier
- Light/dark mode
- Multiple named save files
- Hint system with cooldown
- Manual save only — no auto-save
