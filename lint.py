#!/usr/bin/env python3
"""Lint.py for Sudoku game - enforces layered architecture."""

import ast
import os
import sys
from typing import Dict, List, Set, Tuple

# Layer order (earlier layers can import from later layers only via providers)
LAYER_ORDER = ["types", "config", "utils", "repo", "service", "runtime", "ui"]
LAYER_DIRS = set(LAYER_ORDER) | {"providers"}

# Layer to directory mapping
LAYER_TO_DIR: Dict[str, str] = {
    "types": "src/types",
    "config": "src/config",
    "utils": "src/utils",
    "repo": "src/repo",
    "service": "src/service",
    "runtime": "src/runtime",
    "ui": "src/ui",
    "providers": "src/providers",
}

# Allowed imports per layer (can import from same layer and earlier layers, plus providers for cross-cutting)
ALLOWED_IMPORTS: Dict[str, Set[str]] = {
    "types": {"types"},
    "config": {"types", "config"},
    "utils": {"types", "config", "utils"},
    "providers": {"types", "config", "utils", "providers"},
    "repo": {"types", "config", "utils", "repo", "providers"},
    "service": {"types", "config", "utils", "repo", "service", "providers"},
    "runtime": {"types", "config", "utils", "repo", "service", "providers", "runtime"},
    "ui": {"types", "config", "utils", "service", "runtime", "providers", "ui"},
}


class LintError:
    """Represents a linting error."""
    
    def __init__(self, filepath: str, line: int, message: str):
        self.filepath = filepath
        self.line = line
        self.message = message
    
    def __str__(self) -> str:
        return f"{self.filepath}:{self.line}: {self.message}"


def get_layer(filepath: str) -> str:
    """Determine the layer a file belongs to."""
    rel_path = filepath
    for layer, dir_path in LAYER_TO_DIR.items():
        if rel_path.startswith(dir_path + "/") or rel_path == dir_path:
            return layer
    return ""


def check_layer_exists(filepath: str) -> List[LintError]:
    """Check if file is in a valid layer directory."""
    errors = []
    rel_path = filepath
    
    for layer in LAYER_DIRS:
        if rel_path.startswith(f"src/{layer}/"):
            return errors
    
    # Root level files are OK if they're in root (not in src/)
    if not rel_path.startswith("src/"):
        return errors
    
    # Files in src/ but not in a layer directory are errors
    if rel_path.startswith("src/") and len(rel_path.split("/")) > 1:
        in_layer = False
        for layer in LAYER_DIRS:
            if rel_path.startswith(f"src/{layer}/"):
                in_layer = True
                break
        if not in_layer:
            errors.append(LintError(filepath, 1, f"File must be in a layer directory ({', '.join(sorted(LAYER_DIRS))})"))
    
    return errors


def check_imports(filepath: str, tree: ast.AST) -> List[LintError]:
    """Check that imports respect layer dependencies."""
    errors = []
    layer = get_layer(filepath)
    
    if not layer:
        return errors
    
    allowed = ALLOWED_IMPORTS.get(layer, set())
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                module = alias.name.split('.')[0]
                if module == 'src':
                    # Extract the layer from the import
                    # e.g., src.types, src.config
                    rest = alias.name[4:]  # Skip 'src.'
                    if rest:
                        imported_layer = rest.split('.')[0]
                        if imported_layer not in allowed:
                            errors.append(LintError(
                                filepath, node.lineno,
                                f"Cannot import from layer '{imported_layer}' - only {sorted(allowed)} allowed"
                            ))
        
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module.startswith('src.'):
                rest = node.module[4:]  # Skip 'src.'
                imported_layer = rest.split('.')[0] if rest else ""
                if imported_layer and imported_layer not in allowed:
                    errors.append(LintError(
                        filepath, node.lineno,
                        f"Cannot import from layer '{imported_layer}' - only {sorted(allowed)} allowed"
                    ))
    
    return errors


def check_line_count(filepath: str) -> List[LintError]:
    """Check that file doesn't exceed 300 lines."""
    errors = []
    
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    if len(lines) > 300:
        errors.append(LintError(filepath, len(lines), f"File has {len(lines)} lines, max is 300"))
    
    return errors


def find_python_files() -> List[str]:
    """Find all Python source files in the project."""
    python_files = []
    
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories and common excludes
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('venv', 'env', '__pycache__', 'tests')]
        
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                # Convert to relative path
                if filepath.startswith('./'):
                    filepath = filepath[2:]
                python_files.append(filepath)
    
    return python_files


def lint() -> List[LintError]:
    """Run all lint checks."""
    errors = []
    python_files = find_python_files()
    
    for filepath in python_files:
        # Check file is in layer directory
        layer_errors = check_layer_exists(filepath)
        errors.extend(layer_errors)
        
        # Only parse and check imports for files in src/
        if filepath.startswith('src/'):
            try:
                with open(filepath, 'r') as f:
                    source = f.read()
                
                tree = ast.parse(source)
                
                # Check imports
                import_errors = check_imports(filepath, tree)
                errors.extend(import_errors)
                
                # Check line count
                line_errors = check_line_count(filepath)
                errors.extend(line_errors)
                
            except SyntaxError as e:
                errors.append(LintError(filepath, e.lineno or 1, f"Syntax error: {e.msg}"))
    
    return errors


def main() -> int:
    """Main entry point."""
    errors = lint()
    
    if errors:
        print("Lint failed with the following violations:\n")
        for error in sorted(errors, key=lambda e: (e.filepath, e.line)):
            print(f"  {error}")
        print(f"\n{len(errors)} error(s) found")
        return 1
    else:
        print("Lint passed! No violations found.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
