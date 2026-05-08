"""Game service for Sudoku logic."""

from typing import List, Optional
from src.types import Grid, Cell, Move, GameState, Difficulty
from src.config import GRID_SIZE, SUBGRID_SIZE, MAX_MISTAKES
from src.providers import get_generator
from src.repo import get_repository
from src.utils import is_valid_value, get_empty_cells, is_grid_complete


class GameSession:
    """Manages a single Sudoku game session."""
    
    def __init__(self, difficulty: Difficulty = Difficulty.MEDIUM):
        """
        Initialize a new game session.
        
        Args:
            difficulty: The difficulty level for the puzzle.
        """
        generator = get_generator()
        puzzle = generator.generate_puzzle(difficulty)
        
        self._state = GameState(
            grid=puzzle.seed,
            initial_grid=puzzle.seed,
            moves=[],
            mistakes=0,
            difficulty=difficulty
        )
        self._solution = puzzle.solution
    
    def validate_move(self, cell: Cell, value: int) -> bool:
        """
        Validate if a move is correct.
        
        Args:
            cell: The cell position (row, col).
            value: The value to place.
            
        Returns:
            True if the move is correct, False otherwise.
        """
        row, col = cell
        
        # Check if cell is in initial grid (cannot modify)
        if self._state.initial_grid[row][col] is not None:
            return False
        
        # Check if value matches solution
        return value == self._solution[row][col]
    
    def make_move(self, cell: Cell, value: int) -> bool:
        """
        Make a move on the grid.
        
        Args:
            cell: The cell position (row, col).
            value: The value to place.
            
        Returns:
            True if move was successful, False if invalid.
        """
        row, col = cell
        
        # Check if cell is in initial grid
        if self._state.initial_grid[row][col] is not None:
            return False
        
        # Validate the move
        is_correct = self.validate_move(cell, value)
        
        move = Move(cell=cell, value=value)
        
        if is_correct:
            self._state.grid[row][col] = value
            self._state.moves.append(move)
            return True
        else:
            self._state.mistakes += 1
            return False
    
    def check_victory(self) -> bool:
        """
        Check if the player has won the game.
        
        Returns:
            True if the grid matches the solution, False otherwise.
        """
        return self._state.grid == self._solution
    
    def is_valid_solution(self, grid: Grid) -> bool:
        """
        Check if a given grid is a valid Sudoku solution.
        
        Args:
            grid: The grid to validate.
            
        Returns:
            True if the grid is a valid solution.
        """
        # Check if grid is complete
        if not is_grid_complete(grid):
            return False
        
        # Check rows
        for row in range(9):
            row_values = set()
            for col in range(9):
                val = grid[row][col]
                if val in row_values:
                    return False
                row_values.add(val)
        
        # Check columns
        for col in range(9):
            col_values = set()
            for row in range(9):
                val = grid[row][col]
                if val in col_values:
                    return False
                col_values.add(val)
        
        # Check subgrids
        for box_row in range(3):
            for box_col in range(3):
                subgrid_values = set()
                start_row = box_row * 3
                start_col = box_col * 3
                for row in range(start_row, start_row + 3):
                    for col in range(start_col, start_col + 3):
                        val = grid[row][col]
                        if val in subgrid_values:
                            return False
                        subgrid_values.add(val)
        
        return True
    
    def get_state(self) -> GameState:
        """Get the current game state."""
        return self._state
    
    def get_grid(self) -> Grid:
        """Get the current grid."""
        return self._state.grid
    
    def get_initial_grid(self) -> Grid:
        """Get the initial (unchangeable) grid."""
        return self._state.initial_grid
    
    def is_game_over(self) -> bool:
        """Check if the game is over (max mistakes reached)."""
        return self._state.mistakes >= MAX_MISTAKES
    
    def get_remaining_empty_cells(self) -> List[Cell]:
        """Get list of empty cell positions."""
        return get_empty_cells(self._state.grid)


def create_game(difficulty: Difficulty = Difficulty.MEDIUM) -> GameSession:
    """
    Factory function to create a new game session.
    
    Args:
        difficulty: The difficulty level for the puzzle.
        
    Returns:
        A new GameSession instance.
    """
    return GameSession(difficulty)
