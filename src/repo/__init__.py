"""Sudoku repository for puzzle persistence."""

import json
import os
from typing import List, Optional
from src.types import Puzzle, Difficulty
from src.config import PUZZLE_STORAGE_DIR
from src.providers import get_generator


class SudokuRepository:
    """Repository for storing and retrieving Sudoku puzzles."""
    
    def __init__(self, storage_dir: str = PUZZLE_STORAGE_DIR):
        """
        Initialize the repository.
        
        Args:
            storage_dir: Directory to store puzzle files.
        """
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
    
    def save_puzzle(self, puzzle: Puzzle, difficulty: Difficulty, puzzle_id: Optional[str] = None) -> str:
        """
        Save a puzzle to storage.
        
        Args:
            puzzle: The puzzle to save.
            difficulty: Difficulty level.
            puzzle_id: Optional ID; if None, generates one.
            
        Returns:
            The ID of the saved puzzle.
        """
        if puzzle_id is None:
            puzzle_id = self._generate_puzzle_id()
        
        data = {
            "id": puzzle_id,
            "difficulty": difficulty.value,
            "seed": puzzle.seed,
            "solution": puzzle.solution
        }
        
        filepath = os.path.join(self.storage_dir, f"{puzzle_id}.json")
        with open(filepath, 'w') as f:
            json.dump(data, f)
        
        return puzzle_id
    
    def load_puzzle(self, puzzle_id: str) -> Optional[Puzzle]:
        """
        Load a puzzle by ID.
        
        Args:
            puzzle_id: The ID of the puzzle to load.
            
        Returns:
            The Puzzle if found, None otherwise.
        """
        filepath = os.path.join(self.storage_dir, f"{puzzle_id}.json")
        
        if not os.path.exists(filepath):
            return None
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        return Puzzle(seed=data["seed"], solution=data["solution"])
    
    def list_puzzles(self) -> List[str]:
        """
        List all stored puzzle IDs.
        
        Returns:
            List of puzzle IDs.
        """
        puzzles = []
        for filename in os.listdir(self.storage_dir):
            if filename.endswith('.json'):
                puzzles.append(filename[:-5])  # Remove .json extension
        return puzzles
    
    def generate_and_save_puzzle(self, difficulty: Difficulty) -> str:
        """
        Generate a new puzzle and save it.
        
        Args:
            difficulty: Difficulty level for the puzzle.
            
        Returns:
            The ID of the saved puzzle.
        """
        generator = get_generator()
        puzzle = generator.generate_puzzle(difficulty)
        return self.save_puzzle(puzzle, difficulty)
    
    def _generate_puzzle_id(self) -> str:
        """Generate a unique puzzle ID."""
        import time
        import uuid
        return f"puzzle_{int(time.time())}_{uuid.uuid4().hex[:8]}"


# Module-level repository instance
_repository: Optional[SudokuRepository] = None


def get_repository(storage_dir: Optional[str] = None) -> SudokuRepository:
    """Get the module-level repository instance."""
    global _repository
    if _repository is None:
        _repository = SudokuRepository(storage_dir) if storage_dir else SudokuRepository()
    return _repository
