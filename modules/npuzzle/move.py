from enum import Enum


class Move(Enum):
    """
    Represents a movement in one of four directions
    """

    LEFT = 1
    RIGHT = 2
    DOWN = 3
    UP = 4

    def __str__(self):
        """
        Returns a string representation of the move
        """
        return {self.LEFT: "🠄", self.RIGHT: "🠆", self.DOWN: "🠇", self.UP: "🠅"}[self]

    def reverse(self):
        """
        Returns the opposite of the move
        """
        return {
            self.LEFT: self.RIGHT,
            self.RIGHT: self.LEFT,
            self.DOWN: self.UP,
            self.UP: self.DOWN,
        }[self]
