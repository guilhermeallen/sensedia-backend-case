# Proposal: Fix POST /clientes Validation Error Handling (SSAI-99)

## Why
The `POST /clientes` endpoint returns HTTP 500 when a customer name contains digits. The error is a validation failure, not an internal server error. This is a defect in error handling: the validation logic raises an uncaught `RuntimeError` instead of an `HTTPException` with an appropriate 4xx status, causing the generic exception handler to report a 500 instead of a client error (400/422).

## What Changes
- **Modified:** Error handling in customer creation validation to return `HTTP 400 Bad Request` for invalid name input instead of `HTTP 500 Internal Server Error`.
- Input validation logic remains unchanged until the product team decides whether the "no digits in name" rule should be kept, relaxed, or removed.

## Capabilities

### New Capabilities
- `cliente-validation-error-handling` — proper exception handling for customer creation validation failures

### Modified Capabilities
(None at the requirement level; this is an error handling fix, not a behavior change)

## Impact

**Affected Code:**
- `app/services/cliente_service.py` — `ClienteService.criar_cliente()` method (lines 10-14)

**APIs:**
- `POST /clientes` — now returns `HTTP 400` with validation message for invalid names (instead of 500)

**Interfaces:**
- Client applications calling `POST /clientes` will receive consistent 4xx responses for validation errors

**Dependencies:**
- FastAPI (existing)
- HTTPException (existing)

**No external systems affected**
