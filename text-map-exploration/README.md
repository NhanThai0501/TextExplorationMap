# Text-Based Exploration Game

A text-based adventure game that allows players to navigate a dynamic map, solve puzzles, collect items, and interact with their surroundings.

## Features

- **Dynamic Map**: Navigate through a grid-based map where rooms are connected dynamically based on their coordinates.
- **Item Management**: Pick up, drop, and manage items in your inventory.
- **Puzzle Events**: Encounter and solve puzzles to progress through locked or event-triggered rooms.
- **Interactive Commands**: Use intuitive commands to explore, interact, and make decisions.

## How to Play

### Starting the Game
- Run the game using the following command:
  ```bash
  python main.py

## Development
### File Structure
- main.py: Contains the main game loop and command handling.
- game/map.py: Manages the dynamic map, including room connections and display logic.
- game/player.py: Defines the player class and inventory management.
- game/puzzles.py: Handles puzzles and room events.
**Assets**:
- assets/example_map.json: Defines the map structure, rooms, connections, items, and events.
- assets/puzzles.json: Contains puzzles and events for specific rooms.