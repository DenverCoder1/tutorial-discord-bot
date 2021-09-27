import random
from typing import List, Optional

from .move import Move


class BoardState:
    """
    The state for an n-puzzle contains:
        - the size of the puzzle (eg. 3 for a 3x3 puzzle)
        - a list of integers representing the board
        - a list of moves that have been made
        - the target board

    The target board for an 8-puzzle is:
    ```
    0 1 2
    3 4 5
    6 7 8
    ```
    (where 0 represents the empty tile)
    """

    def __init__(
        self,
        size: int,
        board: Optional[List[int]] = None,
        moves: Optional[List[Move]] = None,
    ):
        """
        Constructor for the state

        Args:
            size: the size of the puzzle
            board: the board layout
            moves: the list of moves that have been made
            target: the target board layout
        """
        self.size = size
        self.target = list(range(size * size))
        self.board = board or self.target.copy()
        self.moves = moves or []

    @classmethod
    def init_from_random(cls, size: int) -> "BoardState":
        """
        Creates a random state by making size^3 moves from the target state

        Args:
            size: the size of the puzzle

        Returns:
            a random initial state
        """
        state = BoardState(size)
        for _ in range(size * size * size):
            state.move_if_legal(random.choice(list(Move)))
        state.moves = []
        return state

    def find_empty_tile(self) -> int:
        """
        Locates the empty tile in the board

        Returns:
            the index of the empty tile
        """
        return self.board.index(0)

    def path_length(self) -> int:
        """
        Returns the number of moves made to get to the state
        """
        return len(self.moves)

    def is_target(self) -> bool:
        """
        Checks if the state is the target state

        Returns:
            true if the state is the target state, false otherwise
        """
        return self.board == self.target

    def swap_tiles(self, tile1: int, tile2: int) -> None:
        """
        Swaps the tiles at the given indices

        Args:
            tile1: the index of the first tile
            tile2: the index of the second tile
        """
        self.board[tile1], self.board[tile2] = self.board[tile2], self.board[tile1]

    def swap_tile_with_empty(self, index: int) -> bool:
        """
        Swaps the tile at the given index with the empty tile

        Args:
            index: the index to swap with empty

        Returns:
            true if the move is legal, false otherwise
        """
        move = None
        empty = self.find_empty_tile()

        if index == empty - 1:
            move = Move.LEFT
        elif index == empty + 1:
            move = Move.RIGHT
        elif index == empty - self.size:
            move = Move.UP
        elif index == empty + self.size:
            move = Move.DOWN

        return self.move_if_legal(move)

    def move_if_legal(self, move: Move) -> bool:
        """
        Moves the empty tile if the move is legal

        Args:
            move: the move to make

        Returns:
            true if the move is legal, false otherwise
        """
        size = self.size
        empty = self.find_empty_tile()
        # checks if the empty tile is not in the first col and the move is to the left
        if empty % size > 0 and move == Move.LEFT:
            self.moves += [Move.LEFT]
            self.swap_tiles(empty, empty - 1)
            return True
        # check if the empty tile is not in the nth col and the move is to the right
        if empty % size < size - 1 and move == Move.RIGHT:
            self.moves += [Move.RIGHT]
            self.swap_tiles(empty, empty + 1)
            return True
        # check if the empty tile is not in the first row and the move is up
        if empty >= size and move == Move.UP:
            self.moves += [Move.UP]
            self.swap_tiles(empty, empty - size)
            return True
        # check if the empty tile is not in the nth row and the move is down
        if empty < size * (size - 1) and move == Move.DOWN:
            self.moves += [Move.DOWN]
            self.swap_tiles(empty, empty + size)
            return True
        return False
