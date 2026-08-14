# Proposal: Fix POST /clientes returning 500 on validation failure

## Why
POST /clientes is returning HTTP 500 when a client name contains digits. The issue occurs because the name validation raises an unhandled `RuntimeError` instead of signaling a validation error (HTTP 400) like other business rules in the same endpoint. This violates the API's error-handling convention and exposes unhandled exceptions to clients instead of structured error responses.

## What Changes
- Fix `ClienteService.criar_cliente()` to raise `HTTPException(status_code=400)` instead of `RuntimeError` when client name contains digits
- Align the name validation exception type with the existing pattern used for duplicate CPF/Email validation
- Add test coverage for the name validation error path to prevent regression

## Capabilities
### New Capabilities
- `client-creation-error-handling` — proper HTTP error response for client name validation failures

### Modified Capabilities
(none)

## Impact
- **Code changed:** `app/services/cliente_service.py` (the `criar_cliente` method)
- **APIs affected:** `POST /api/v1/clientes` (error response behavior only, success path unchanged)
- **Database:** no schema or data migrations needed
- **Dependencies:** no new dependencies added
- **Backward compatibility:** breaking (error response status code changes from 500 to 400), but this is a defect fix — clients were receiving unhandled exceptions; the new behavior is the correct one
- **Tests:** new unit tests added for name validation error case; existing functionality tests remain unchanged
