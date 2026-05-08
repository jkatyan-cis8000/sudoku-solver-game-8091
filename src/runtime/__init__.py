"""Application runtime for Sudoku game."""

from src.types import Difficulty, Grid
from src.providers import SudokuGenerator
from src.repo import SudokuRepository
from src.service import GameSession

MAX_MISTAKES = 3


class Application:
    """Orchestrates the Sudoku game application."""
    
    def __init__(self):
        """Initialize the application."""
        self._session: GameSession | None = None
        self._difficulty = Difficulty.MEDIUM
        self._generator = SudokuGenerator()
        self._repo = SudokuRepository()
    
    def set_difficulty(self, difficulty: Difficulty) -> None:
        """
        Set the game difficulty.
        
        Args:
            difficulty: The difficulty level.
        """
        self._difficulty = difficulty
    
    def start_new_game(self) -> None:
        """Start a new game session with a generated puzzle."""
        puzzle = self._generator.generate_puzzle(self._difficulty)
        self._session = GameSession(puzzle)
    
    def load_game(self, puzzle_id: str) -> bool:
        """
        Load a saved game.
        
        Args:
            puzzle_id: The ID of the puzzle to load.
            
        Returns:
            True if loaded successfully, False otherwise.
        """
        puzzle = self._repo.load_puzzle(puzzle_id)
        if puzzle is None:
            return False
        self._session = GameSession(puzzle)
        return True
    
    def save_game(self, puzzle_id: str) -> bool:
        """
        Save the current game.
        
        Args:
            puzzle_id: The ID to save under.
            
        Returns:
            True if saved successfully.
        """
        if self._session is None:
            return False
        puzzle = self._session.get_puzzle()
        self._repo.save_puzzle(puzzle_id, puzzle)
        return True
    
    def make_move(self, cell: tuple[int, int], value: int) -> bool:
        """
        Attempt to make a move.
        
        Args:
            cell: The (row, col) cell to fill.
            value: The value to place.
            
        Returns:
            True if the move was valid, False otherwise.
        """
        if self._session is None:
            return False
        return self._session.make_move(cell, value)
    
    def get_state(self) -> tuple[Grid, int, int]:
        """
        Get current game state.
        
        Returns:
            Tuple of (grid, mistakes, max_mistakes).
        """
        if self._session is None:
            raise RuntimeError("No game in progress")
        return (self._session.get_grid(), 
                self._session.get_mistakes(), 
                MAX_MISTAKES)
    
    def is_game_over(self) -> bool:
        """Check if the game is over (too many mistakes)."""
        if self._session is None:
            return True
        return self._session.get_mistakes() >= MAX_MISTAKES
    
    def check_victory(self) -> bool:
        """Check if the puzzle is solved correctly."""
        if self._session is None:
            return False
        return self._session.is_solved()
    
    def get_solution(self) -> Grid:
        """
        Get the solution grid.
        
        Returns:
            The complete solution grid.
        """
        if self._session is None:
            raise RuntimeError("No game in progress")
        return self._session.get_solution()
