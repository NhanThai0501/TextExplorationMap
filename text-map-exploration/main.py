from game.map import Map
from game.puzzles import Puzzles
from game.player import Player
from colorama import Fore, Style

puzzles = Puzzles("assets/puzzles.json")

def handle_event(event, player):
    if event == "locked":
        print("The room is locked! You need a key to enter.")
        if "key" in player.inventory:
            print("You used the key to unlock the room!")
            return True
        return False
    else:
        return getattr(puzzles, event)()

def game_loop(player, game_map):
    """
    Main game loop.
    """
    def quit_game(args):
        print("Thanks for playing!")
        return False  # Ends the loop

    def show_help(args):
        print("Available Commands:")
        print("- move <direction>: Move to a connected room (north, south, east, west).")
        print("- pick <item>: Pick up a specific item in the current room.")
        print("- pick all: Pick up all items in the current room.")
        print("- inventory: Show your current inventory.")
        print("- drop <item>: Drop an item from your inventory.")
        print("- show map: Display the current map.")
        print("- reveal map: Display the entire map with all rooms.")
        print("- describe: Show a detailed description of the current room.")
        print("- quit: Exit the game.")

    def show_map(args):
        game_map.display_map(player, is_full_map=False)

    def reveal_map(args):
        game_map.display_map(player, is_full_map=True)

    def move_player(args):
        direction = args[0] if args else None
        current_room = game_map.game_map[player.position]
        if direction in current_room.connections:
            new_position = current_room.connections[direction]
            if new_position:
                player.position = new_position
                print(f"Moved to {new_position}")
            else:
                print(Fore.RED + "That direction is blocked!" + Style.RESET_ALL)
        else:
            print(Fore.RED + "Invalid direction!" + Style.RESET_ALL)

    def pick_item(args):
        current_room = game_map.game_map[player.position]
        if args[0] == "all":
            if current_room.items:
                player.inventory.extend(current_room.items)
                print(f"You picked up all items: {', '.join(current_room.items)}")
                current_room.items.clear()
            else:
                print("There are no items to pick up.")
        else:
            item = args[0] if args else None
            if item in current_room.items:
                player.inventory.append(item)
                current_room.items.remove(item)
                print(f"You picked up {item}.")
            else:
                print("That item is not here.")

    def show_inventory(args):
        if player.inventory:
            print(f"Your inventory: {', '.join(player.inventory)}")
        else:
            print("Your inventory is empty.")

    def drop_item(args):
        current_room = game_map.game_map[player.position]
        item = args[0] if args else None
        if item in player.inventory:
            player.inventory.remove(item)
            current_room.items.append(item)
            print(f"You dropped {item}.")
        else:
            print("You don't have that item.")

    def reset_player(args):
        player.position = (0, 0)  # Assuming the starting position is (0, 0)
        player.inventory.clear()
        print("You have been reset to the starting position. Your inventory is now empty.")

    def describe_room(args):
        current_room = game_map.game_map[player.position]
        connections = ", ".join([f"{direction}: {dest}" for direction, dest in current_room.connections.items() if dest])
        print(f"Room: {current_room.description}")
        print(f"Connections: {connections}")
        if current_room.items:
            print(f"Items: {', '.join(current_room.items)}")
        if current_room.event:
            print(f"Event: {current_room.event}")
            handle_event(current_room.event, player)
            
    # def describe_room(player, game_map):
    #     """
    #     Shows the current room's description and possible movements.
    #     """
    #     current_room = game_map.game_map[player.position]
    #     print(f"Description: {current_room.description}")
    #     accessible_directions = [
    #         direction for direction, target in current_room.connections.items() if target
    #     ]
    #     print(f"Possible directions to move: {', '.join(accessible_directions)}")

            
    def show_stats(args):
        print("Your stats:")
        print(f"- Position: {player.position}")
        print(f"- Inventory: {', '.join(player.inventory)}")

    # Command dispatch table
    commands = {
        "quit": quit_game,
        "help": show_help,
        "show map": show_map,
        "reveal map": reveal_map,
        "move": move_player,
        "pick": pick_item,
        "inventory": show_inventory,
        "drop": drop_item,
        "reset": reset_player,
        "describe": describe_room,
        "stat": show_stats
    }

    # Main game loop
    running = True
    while running:
        current_room = game_map.game_map[player.position]
        print(f"You are in {current_room.description}")
        if current_room.items:
            print(f"You see the following items: {', '.join(current_room.items)}")

        # Parse the command
        command = input("Enter command: ").strip().lower()
        command_name = command if command in commands else command.split(" ", 1)[0]
        command_args = command.split(" ")[1:] if " " in command else []

        # Execute the command
        if command_name in commands:
            result = commands[command_name](command_args)
            if result is False:  # If the command returns False, exit the loop
                running = False
        else:
            print("Unknown command! Type 'help' for a list of available commands.")


if __name__ == "__main__":
    map_file = "assets/example_map.json"  # Update the file path to JSON

    # Initialize the Map
    game_map = Map()
    game_map.load_map_from_json(map_file)  # Load from JSON
    game_map.link_room_connections()

    # Initialize the player
    player = Player((0, 0))  # Starting position
    
    # Start the game loop
    game_loop(player, game_map)
