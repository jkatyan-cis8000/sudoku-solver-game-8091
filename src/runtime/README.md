# Runtime Layer

App lifecycle, orchestration, and dependency wiring.

This layer coordinates all components and manages application lifecycle.

## What belongs here

- Application startup/shutdown
- Dependency injection
- Component orchestration
- Main entry point

## Rules

- May import from: `types`, `config`, `repo`, `service`, `providers`, `runtime`
- Entry point for the application
- No business logic
