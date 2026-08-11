# Proposal: Fix HTTP 500 Errors in POST /clientes by Correcting Error Handling

## Why
The POST /clientes endpoint returns HTTP 500 Internal Server Error when the client name contains digits, instead of a proper HTTP 400 Bad Request. This is a defect in error handling consistency — the validation logic is correct, but the exception type is wrong. The same service has two other validation rules that correctly raise HTTPException with 400 status; the digit-in-name rule breaks the pattern by raising an unhandled RuntimeError, which bubbles up as a 500.

## What Changes
- The `ClienteService.criar_cliente` method will raise `HTTPException(status_code=400)` instead of `RuntimeError` when the client name contains digits
- This aligns the error handling with sibling validations (CPF and email uniqueness checks) in the same method
- The HTTP response becomes semantically correct (4xx for client error, not 5xx for server error)

## Capabilities
- **New Capabilities**: `error-handling-consistency` — correction to ensure all client-creation validations return consistent HTTP status codes

## Impact
- Affected code: `app/services/cliente_service.py::ClienteService.criar_cliente` method
- Affected API: `POST /api/v1/clientes`
- Response status: changes from 500 to 400 for invalid names
- No database schema changes, no dependency changes, no API contract breakage (4xx is semantically correct)
- Testing: no test suite exists; validation via manual testing and code review
