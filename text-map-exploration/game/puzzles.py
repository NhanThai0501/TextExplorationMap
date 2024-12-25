import json
import random
import sys  # For exiting the game on GAME OVER


class Puzzles:
    def __init__(self, file_path="assets/puzzles.json"):
        """
        Initialize the Puzzles class and load puzzles from a JSON file.
        """
        self.chances = 5  # Number of chances for a player to solve a puzzle
        self.puzzles = self.load_puzzles(file_path)

    def load_puzzles(self, file_path):
        """
        Load puzzles from the JSON file.
        """
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: Puzzle file {file_path} not found.")
            return {}

    def retry_with_hint(self, puzzle_name):
        """
        Handles retries for a puzzle. Randomly selects a variation of the puzzle
        and gives hints after 3 failures. Ends the game after 5 failures.
        """
        if puzzle_name not in self.puzzles:
            print(f"No puzzles found for type: {puzzle_name}")
            return False

        puzzle = random.choice(self.puzzles[puzzle_name])
        question, answer, hint = puzzle["question"], puzzle["answer"], puzzle["hint"]
        
        attempts = 0
        while attempts < self.chances:
            print(f"Puzzle: {question}")
            user_answer = input("Your answer: ").strip()
            if user_answer.lower() == answer.lower():
                print("Correct! You solved the puzzle.")
                return True
            attempts += 1
            print(f"Incorrect. You have {self.chances - attempts} attempts remaining.")
            if attempts == 3:
                print(f"Hint: {hint}")
        
        print("GAME OVER. You've used all your attempts.")
        sys.exit()  # End the game

    def math_puzzle(self):
        return self.retry_with_hint("math_puzzle")

    def find_symbol_puzzle(self):
        return self.retry_with_hint("find_symbol_puzzle")

    def pattern_recognition(self):
        return self.retry_with_hint("pattern_recognition")

    def math_series(self):
        return self.retry_with_hint("math_series")

    def shape_counting(self):
        return self.retry_with_hint("shape_counting")

    def cryptogram(self):
        return self.retry_with_hint("cryptogram")

    def odd_one_out(self):
        return self.retry_with_hint("odd_one_out")

    def true_or_false(self):
        return self.retry_with_hint("true_or_false")

    def matching(self):
        return self.retry_with_hint("matching")

    def equation_balancing(self):
        return self.retry_with_hint("equation_balancing")
