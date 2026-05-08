"""Type definitions for Sudoku game."""

from dataclasses import dataclass
from typing import NewType, List, Optional, Tuple
from enum import Enum


# Grid type: 9x9 matrix where each cell is optional int (None for empty)
Grid = List[List[Optional[int]]]

# Cell identifier
Cell = NewType("Cell", Tuple[int, int])  # (row, col)


class Difficulty(Enum):
    """Difficulty levels for puzzle generation."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"


@dataclass
class Puzzle:
    """A Sudoku puzzle with its solution."""
    seed: Grid  # Initial puzzle state
    solution: Grid  # Complete solved grid


@dataclass
class Move:
    """A player's move on the grid."""
    cell: Cell
    value: int
    timestamp: float = 0.0  # Optional timestamp


@dataclass
class GameState:
    """Current game state."""
    grid: Grid
    initial_grid: Grid  # Unchangeable cells
    moves: List[Move]
    mistakes: int
    difficulty: Difficulty
