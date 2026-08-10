# Proposal — SSAI-94: POST /clientes Error Handling Inconsistency

## Why
The `POST /clientes` endpoint returns HTTP 500 (Internal Server Error) when a client name contains numeric digits (e.g., "João da Si4lva"). The root cause is that the name validation in `ClienteService.criar_cliente()` raises a bare `RuntimeError` instead of an `HTTPException` with a 4xx status code, breaking the consistent error-handling pattern used by sibling validation rules (duplicate CPF, duplicate email) which correctly return HTTP 400.

## What Changes
- **Modified:** `ClienteService.criar_cliente()` method's name validation error handling
  - Replaces bare `RuntimeError` with `HTTPException(status_code=400)` to match the pattern used by CPF and email validation
  - Ensures the endpoint returns a proper client error (4xx) instead of server error (5xx) for validation failures

## Capabilities

### Modified Capabilities
- **client-registration-validation** — Error handling consistency for validation rules in client creation

## Impact
- **Code:** `app/services/cliente_service.py` (criar_cliente method)
- **Affected APIs:** `POST /clientes`
- **Dependencies:** None (existing fastapi, HTTPException)
- **Breaking Changes:** None — the endpoint will now return 400 instead of 500 for names with digits
- **Database:** No schema or model changes
