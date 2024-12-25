class Player:
    def __init__(self, start_position):
        self.position = start_position
        self.inventory = []
        self.visited_rooms = set()  # Keep track of visited rooms

    def visit_room(self, position):
        self.visited_rooms.add(position)
