# Providers Layer

Cross-cutting concerns: auth, telemetry, connectors, flags.

This layer handles external services and infrastructure concerns.

## What belongs here

- Puzzle generators
- External API clients
- Telemetry/tracing
- Feature flags

## Rules

- May import from: `types`, `config`, `utils`, `providers`
- No business logic
- No UI concerns
