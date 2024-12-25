import json
from .room import Room
from colorama import Fore, Style


class Map:
    def __init__(self):
        self.game_map = {}  # Stores the rooms as a dictionary
        self.map_size = 0  # Dimensions of the map
        self.visited_rooms = set()  # Set of visited rooms
        self.player_position = (0, 0)  # Default starting position

    def calculate_map_size(self, json_data):
        """
        Calculates the map dimensions dynamically from the JSON data.
        """
        max_row = max(room["coordinates"][0] for room in json_data["map"])
        max_col = max(room["coordinates"][1] for room in json_data["map"])
        self.map_height = max_row + 1  # Rows are based on maximum row index
        self.map_width = max_col + 1  # Columns are based on maximum column index
        # print(f"[DEBUG]: Calculated map size: {self.map_height}x{self.map_width}")



    def load_map_from_json(self, file_path):
        """
        Loads the map from a JSON file.
        """
        with open(file_path, "r") as f:
            data = json.load(f)
            self.calculate_map_size(data) # Calculate map size based on JSON data
            for room_data in data["map"]:
                coordinates = tuple(room_data["coordinates"])
                description = room_data["description"]
                items = room_data.get("items", [])
                event = room_data.get("event", None)
                
                # Initialize connections as a dictionary
                connections = {direction: True for direction in room_data["connections"]}
                
                self.game_map[coordinates] = Room(coordinates, description, connections, items, event)
                # print(f"[DEBUG]: Loaded Room: {coordinates}, Connections: {connections}")


    def link_room_connections(self):
        """
        Dynamically establishes connections between adjacent rooms.
        """
        moves = {"north": (-1, 0), "south": (1, 0), "west": (0, -1), "east": (0, 1)}
        for position, room in self.game_map.items():
            for direction, connected in room.connections.items():
                if connected:  # If marked as connected (True)
                    new_position = (
                        position[0] + moves[direction][0],
                        position[1] + moves[direction][1],
                    )
                    if new_position in self.game_map:
                        room.connections[direction] = new_position
                    else:
                        room.connections[direction] = None
                else:
                    room.connections[direction] = None
            # print(f"[DEBUG]: Room {position} linked connections: {room.connections}")


    # def display_map(self, player, is_full_map=False):
    #     """
    #     Displays the map with room connections and player position.
    #     """
    #     horizontal_borders = [["   " for _ in range(self.map_width)] for _ in range(self.map_height + 1)]
    #     vertical_borders = [[" " for _ in range(self.map_width + 1)] for _ in range(self.map_height)]

    #     # Build the grid based on room connections
    #     for position, room in self.game_map.items():
    #         row, col = position

    #         # Debug bounds
    #         if row < 0 or row >= self.map_height or col < 0 or col >= self.map_width:
    #             # print(f"[ERROR]: Out-of-bounds room position: {position}")
    #             continue

    #         # North Connection
    #         if "north" in room.connections and room.connections["north"] and row > 0:
    #             horizontal_borders[row][col] = Fore.WHITE + "---" + Style.RESET_ALL
    #         else:
    #             horizontal_borders[row][col] = Fore.RED + "---" + Style.RESET_ALL

    #         # South Connection
    #         if "south" in room.connections and room.connections["south"] and row < self.map_height - 1:
    #             horizontal_borders[row + 1][col] = Fore.WHITE + "---" + Style.RESET_ALL
    #         else:
    #             horizontal_borders[row + 1][col] = Fore.RED + "---" + Style.RESET_ALL

    #         # West Connection
    #         if "west" in room.connections and room.connections["west"] and col > 0:
    #             vertical_borders[row][col] = Fore.WHITE + "|" + Style.RESET_ALL
    #         else:
    #             vertical_borders[row][col] = Fore.RED + "|" + Style.RESET_ALL

    #         # East Connection
    #         if "east" in room.connections and room.connections["east"] and col < self.map_width - 1:
    #             vertical_borders[row][col + 1] = Fore.WHITE + "|" + Style.RESET_ALL
    #         else:
    #             vertical_borders[row][col + 1] = Fore.RED + "|" + Style.RESET_ALL

    #     # Print the map
    #     print("\nFull Map:" if is_full_map else "\nCurrent Map:")
    #     print("    " + "   ".join([f"{i}" for i in range(self.map_width)]))
    #     for row in range(self.map_height):
    #         row_display = f"{Fore.WHITE}{row}{Style.RESET_ALL} " + Fore.CYAN + "|" + Style.RESET_ALL
    #         for col in range(self.map_width):
    #             if (row, col) == player.position and not is_full_map:
    #                 cell = Fore.BLUE + " P " + Style.RESET_ALL  # Player position
    #             elif is_full_map or (row, col) in self.visited_rooms:
    #                 cell = Fore.GREEN + " . " + Style.RESET_ALL  # Visited room or all rooms (Full Map)
    #             else:
    #                 cell = "   "
    #             row_display += cell + vertical_borders[row][col + 1]
    #         print(row_display)
    #     print(Fore.CYAN + "  +" + "+".join(horizontal_borders[self.map_height]) + "+" + Style.RESET_ALL)
    
    def display_map(self, player, is_full_map=False):
        """
        Displays the map grid with clear aesthetics and updates blocked connections dynamically.
        """
        map_display = []

        # Add top border
        top_border = "   " + "+---" * self.map_width + "+"
        map_display.append(top_border)

        # Generate rows with horizontal and vertical connections
        for row in range(self.map_height):
            # Room row
            room_row = f" {row} |"
            for col in range(self.map_width):
                if (row, col) == player.position:
                    cell = f" {Fore.BLUE}P{Style.RESET_ALL} "  # Player position
                elif is_full_map or (row, col) in self.visited_rooms:
                    cell = f" {Fore.GREEN}.{Style.RESET_ALL} "  # Visited rooms
                else:
                    cell = "   "  # Unvisited rooms
                room_row += cell + "|"
            map_display.append(room_row)

            # Horizontal connection row
            if row < self.map_height - 1:
                connection_row = "   +"
                for col in range(self.map_width):
                    # Check the south connection for each room
                    position = (row, col)
                    if position in self.game_map:
                        room = self.game_map[position]
                        if "south" in room.connections and room.connections["south"]:
                            connection_row += "---+"
                        else:
                            connection_row += f"{Fore.RED}---{Style.RESET_ALL}+"
                    else:
                        connection_row += "---+"
                map_display.append(connection_row)

        # Add bottom border
        bottom_border = "   " + "+---" * self.map_width + "+"
        map_display.append(bottom_border)

        # Print the entire map
        print("\n".join(map_display))





