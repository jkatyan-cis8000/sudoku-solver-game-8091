# Repo Layer

Data access layer: DB, files, external state.

This layer handles all data persistence and retrieval operations.

## What belongs here

- Repository classes
- Database connections
- File I/O operations
- External API clients

## Rules

- May import from: `types`, `config`, `repo`
- No business logic
- Pure data access concerns only
