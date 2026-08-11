# Proposal: Fix Client Name Validation Error Handling

## Why

The API endpoint `POST /clientes` is returning HTTP 500 (Internal Server Error) when a client name contains numeric digits. The underlying validation rule is correct, but the exception is not being mapped to an appropriate HTTP status code (4xx), causing the error to escape as a 500. This needs to be corrected to return HTTP 400 (Bad Request) with a clear error message, aligning with the error-handling pattern used by other validation rules in the same service.

## What Changes

- **Modified:** `ClienteService.criar_cliente()` — the client name validation exception is now wrapped in an `HTTPException` with status code 400 instead of raising a bare `RuntimeError`.
- **Impact:** Clients attempting to register with names containing digits will now receive HTTP 400 with a clear validation error message instead of HTTP 500.
- **No schema, dependency, or migration changes.**

## Capabilities

### New Capabilities
- None — this is a correction of existing behavior.

### Modified Capabilities
- `cliente-error-handling` — the name validation error is now properly categorized as a client error (4xx) instead of a server error (5xx).

## Impact

- **Affected code:** `app/services/cliente_service.py`, specifically the `criar_cliente()` method.
- **Affected APIs:** `POST /clientes` (client creation endpoint).
- **No breaking changes:** existing code (other services, repositories, models) is unchanged.
- **Testing:** requires new test case(s) to verify the error response status and message.
- **No new dependencies or migrations required.**
