"""Configuration constants for Sudoku game."""

from typing import Dict
from src.types import Difficulty

# Grid dimensions
GRID_SIZE: int = 9
SUBGRID_SIZE: int = 3

# Puzzle difficulty settings (number of holes to create)
DIFFICULTY_HOLES: Dict[Difficulty, int] = {
    Difficulty.EASY: 30,
    Difficulty.MEDIUM: 40,
    Difficulty.HARD: 50,
    Difficulty.EXPERT: 60,
}

# Default difficulty
DEFAULT_DIFFICULTY: Difficulty = Difficulty.MEDIUM

# Valid values for cells
VALID_VALUES: range = range(1, GRID_SIZE + 1)

# Maximum number of allowed mistakes before game over
MAX_MISTAKES: int = 3

# Puzzle file storage
PUZZLE_STORAGE_DIR: str = "puzzles"
