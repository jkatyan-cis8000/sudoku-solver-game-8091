# UI Layer

User-facing surfaces: CLI, web, GUI.

This layer handles all user interface concerns.

## What belongs here

- CLI interface
- Web UI components
- GUI elements
- User input handling

## Rules

- May import from: `types`, `config`, `service`, `runtime`, `providers`, `ui`
- No business logic
- No data persistence concerns
