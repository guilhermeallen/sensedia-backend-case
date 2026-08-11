# Proposal: Fix Client Validation Error Handling

## Why
The `POST /clientes` endpoint returns HTTP 500 (Internal Server Error) when the client name contains digits, rather than returning a semantically correct 4xx error. The backend raises an unhandled `RuntimeError` that the global exception handler catches and returns as a 500. Other validation rules in the same function correctly raise `HTTPException` with HTTP 400, creating an inconsistency.

## What Changes
- **ClienteService.criar_cliente()** — Change name validation to raise `HTTPException` with HTTP 422 instead of `RuntimeError`
- **ClienteService.atualizar_cliente()** — Add name validation with same 422 error to prevent inconsistent behavior during client updates
- Return consistent error detail messages for all validation failures

## Capabilities
### New Capabilities
- `client-name-validation` — enforce name validation consistently across create and update operations, with proper HTTP error codes

### Modified Capabilities
(none at the requirement level — this is a fix to existing behavior, not a new feature)

## Impact
- **Affected Code:** `app/services/cliente_service.py` (create and update methods)
- **APIs:** `POST /clientes`, `PUT /clientes/{id}`, `PATCH /clientes/{id}`
- **Error Responses:** Will now return HTTP 422 instead of 500 for invalid client names
- **Dependencies:** None new — uses existing FastAPI/Pydantic stack
- **Backwards Compatibility:** Consumers expecting 500 will now receive 422; this is a correction, not a breaking change (500 should never be considered valid API contract)
- **Tests:** Will add tests to cover name validation in both create and update paths
