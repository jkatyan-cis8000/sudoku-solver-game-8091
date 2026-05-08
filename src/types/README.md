# Types Layer

Pure type definitions; no logic or business rules.

This layer contains all data models and type definitions used throughout the application.

## What belongs here

- Dataclasses and namedtuples
- Type aliases
- Enumerations
- Type guards

## Rules

- No imports from internal layers (only `types` itself)
- No business logic
- No side effects
- Pure type definitions only
