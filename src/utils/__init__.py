"""Utility functions for Sudoku game."""

from typing import List, Optional
from src.types import Grid, Cell


def is_valid_value(row: int, col: int, val: int, grid: Grid) -> bool:
    """
    Check if placing val at grid[row][col] is valid.
    Returns True if value doesn't conflict with row, column, or subgrid.
    """
    # Check row
    for c in range(9):
        if c != col and grid[row][c] == val:
            return False
    
    # Check column
    for r in range(9):
        if r != row and grid[r][col] == val:
            return False
    
    # Check 3x3 subgrid
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if (r != row or c != col) and grid[r][c] == val:
                return False
    
    return True


def get_row_cells(grid: Grid, row: int) -> List[int]:
    """Get all values in a row."""
    return [grid[row][col] for col in range(9) if grid[row][col] is not None]


def get_col_cells(grid: Grid, col: int) -> List[int]:
    """Get all values in a column."""
    return [grid[row][col] for row in range(9) if grid[row][col] is not None]


def get_subgrid_cells(grid: Grid, row: int, col: int) -> List[int]:
    """Get all values in the 3x3 subgrid containing (row, col)."""
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    cells = []
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if grid[r][c] is not None:
                cells.append(grid[r][c])
    return cells


def copy_grid(grid: Grid) -> Grid:
    """Create a deep copy of the grid."""
    return [[cell for cell in row] for row in grid]


def get_empty_cells(grid: Grid) -> List[Cell]:
    """Get all empty cell positions in the grid."""
    cells = []
    for row in range(9):
        for col in range(9):
            if grid[row][col] is None:
                cells.append((row, col))
    return cells


def count_filled_cells(grid: Grid) -> int:
    """Count the number of filled cells in the grid."""
    count = 0
    for row in grid:
        for cell in row:
            if cell is not None:
                count += 1
    return count


def is_grid_complete(grid: Grid) -> bool:
    """Check if the grid has no empty cells."""
    for row in grid:
        for cell in row:
            if cell is None:
                return False
    return True


def grid_to_string(grid: Grid) -> str:
    """Convert grid to a readable string representation."""
    lines = []
    for row_idx, row in enumerate(grid):
        if row_idx > 0 and row_idx % 3 == 0:
            lines.append("------+-------+------")
        line_parts = []
        for col_idx, cell in enumerate(row):
            if col_idx > 0 and col_idx % 3 == 0:
                line_parts.append("|")
            line_parts.append(str(cell) if cell is not None else ".")
        lines.append(" ".join(line_parts))
    return "\n".join(lines)
