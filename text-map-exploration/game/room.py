class Room:
    def __init__(self, id, description, connections, items=None, event=None):
        self.id = id
        self.description = description
        self.connections = connections  # Directions and linked rooms
        self.items = items or []  # Items in the room
        self.event = event  # Event or puzzle in the room
        self.has_hidden_item = any(item == "hidden" for item in self.items)
