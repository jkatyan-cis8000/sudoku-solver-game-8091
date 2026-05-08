"""CLI interface for Sudoku game."""

from src.types import Grid
from src.utils import grid_to_string


class SudokuCLI:
    """CLI interface for interacting with Sudoku games."""
    
    def display_grid(self, grid: Grid) -> None:
        """
        Display the Sudoku grid.
        
        Args:
            grid: The 9x9 grid to display.
        """
        print("\n" + grid_to_string(grid) + "\n")
    
    def display_message(self, message: str) -> None:
        """
        Display a message to the user.
        
        Args:
            message: The message to display.
        """
        print(message)
    
    def get_position_input(self) -> tuple[int, int] | None:
        """
        Get user input for a cell position.
        
        Returns:
            A (row, col) tuple or None if input is invalid.
        """
        try:
            row = int(input("Enter row (0-8): "))
            col = int(input("Enter column (0-8): "))
            
            if not (0 <= row <= 8 and 0 <= col <= 8):
                self.display_message("Invalid position. Enter values 0-8.")
                return None
            
            return (row, col)
        except ValueError:
            self.display_message("Invalid input. Please enter numbers.")
            return None
    
    def get_value_input(self) -> int | None:
        """
        Get user input for a cell value.
        
        Returns:
            An integer 1-9 or None if input is invalid.
        """
        try:
            value = int(input("Enter value (1-9): "))
            
            if not (1 <= value <= 9):
                self.display_message("Invalid value. Enter 1-9.")
                return None
            
            return value
        except ValueError:
            self.display_message("Invalid input. Please enter a number.")
            return None
    
    def display_game_status(self, mistakes: int, max_mistakes: int) -> None:
        """
        Display current game status.
        
        Args:
            mistakes: Current number of mistakes.
            max_mistakes: Maximum allowed mistakes.
        """
        self.display_message(f"Mistakes: {mistakes}/{max_mistakes}")
    
    def display_victory(self) -> None:
        """Display victory message."""
        self.display_message("\nCongratulations! You solved the puzzle!")
    
    def display_game_over(self) -> None:
        """Display game over message."""
        self.display_message("\nGame over! Too many mistakes.")
    
    def prompt_continue(self) -> bool:
        """
        Ask user if they want to continue.
        
        Returns:
            True if yes, False otherwise.
        """
        response = input("Play again? (y/n): ").strip().lower()
        return response in ('y', 'yes')
    
    def display_solution(self, solution: Grid) -> None:
        """
        Display the solution grid.
        
        Args:
            solution: The complete solution grid.
        """
        print("\nSolution:")
        self.display_grid(solution)
