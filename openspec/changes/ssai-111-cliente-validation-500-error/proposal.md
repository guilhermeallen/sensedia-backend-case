# Proposal: Fix POST /clientes returning 500 on validation errors

## Why

The `POST /clientes` endpoint is returning HTTP 500 (Internal Server Error) when the backend rejects a client name containing digits. The underlying validation logic is correct — rejecting names with digits is an intentional business rule — but the error is raised as an unhandled `RuntimeError` instead of a proper HTTP 400 Bad Request, causing the API to report a server error instead of a validation failure. This violates the API's contract and the HTTP specification (5xx errors indicate server malfunctions, not invalid input), and confuses clients about the nature of the problem.

## What Changes

- **Modified:** error handling in `ClienteService.criar_cliente()` to raise `HTTPException(status_code=400)` instead of `RuntimeError` when a client name contains digits
- **Modified:** error message to clearly indicate the validation reason (customer names must not contain digits)
- **No functional change:** the validation rule itself remains; names with digits continue to be rejected, consistent with the business logic

## Capabilities

### Modified Capabilities
- `client-validation` — validation error responses now return 4xx instead of 5xx

## Impact

- **Code:** `app/services/cliente_service.py` (one method)
- **API behavior:** `POST /clientes` now returns 400 with clear message instead of 500 when name contains digits
- **Logging:** exception is logged as a validation error, not an unhandled exception, improving observability
- **Database:** no schema changes
- **Dependencies:** no new dependencies
