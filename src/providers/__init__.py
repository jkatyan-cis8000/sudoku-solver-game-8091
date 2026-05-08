"""Sudoku puzzle generator provider."""

import random
from typing import List, Optional, Tuple
from src.types import Grid, Puzzle, Difficulty
from src.config import GRID_SIZE, DIFFICULTY_HOLES
from src.utils import is_valid_value, copy_grid, get_empty_cells


class SudokuGenerator:
    """Generates valid Sudoku puzzles using backtracking algorithm."""
    
    def __init__(self):
        self._solution_count = 0
        self._max_solutions = 2  # Stop after finding multiple solutions
    
    def generate_puzzle(self, difficulty: Difficulty = Difficulty.MEDIUM) -> Puzzle:
        """
        Generate a new Sudoku puzzle with the given difficulty.
        
        Args:
            difficulty: The difficulty level for the puzzle.
            
        Returns:
            A Puzzle containing the seed (incomplete) and solution (complete).
        """
        # Generate a complete valid solution
        solution = self._generate_complete_grid()
        
        # Create puzzle by removing cells
        holes = DIFFICULTY_HOLES.get(difficulty, DIFFICULTY_HOLES[Difficulty.MEDIUM])
        seed = self._remove_cells(copy_grid(solution), holes)
        
        return Puzzle(seed=seed, solution=solution)
    
    def _generate_complete_grid(self) -> Grid:
        """Generate a complete valid Sudoku grid using backtracking."""
        grid = [[None for _ in range(9)] for _ in range(9)]
        self._fill_grid(grid)
        return grid
    
    def _fill_grid(self, grid: Grid) -> bool:
        """Fill the grid with a valid solution using backtracking."""
        empty = self._find_empty(grid)
        if not empty:
            return True  # Grid is complete
        
        row, col = empty
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        
        for num in numbers:
            if is_valid_value(row, col, num, grid):
                grid[row][col] = num
                
                if self._fill_grid(grid):
                    return True
                
                grid[row][col] = None
        
        return False
    
    def _find_empty(self, grid: Grid) -> Optional[Tuple[int, int]]:
        """Find the first empty cell in the grid."""
        for row in range(9):
            for col in range(9):
                if grid[row][col] is None:
                    return (row, col)
        return None
    
    def _remove_cells(self, grid: Grid, holes: int) -> Grid:
        """
        Remove cells from the grid to create the puzzle.
        Ensures the puzzle has a unique solution.
        """
        cells_to_remove = self._get_cells_to_remove(grid, holes)
        
        for row, col in cells_to_remove:
            grid[row][col] = None
        
        return grid
    
    def _get_cells_to_remove(self, grid: Grid, holes: int) -> List[Tuple[int, int]]:
        """Get list of cell positions to remove."""
        # Get all cell positions
        all_cells = [(row, col) for row in range(9) for col in range(9)]
        random.shuffle(all_cells)
        
        # Remove holes cells
        return all_cells[:holes]


# Module-level generator instance
_generator: Optional[SudokuGenerator] = None


def get_generator() -> SudokuGenerator:
    """Get the module-level generator instance."""
    global _generator
    if _generator is None:
        _generator = SudokuGenerator()
    return _generator
