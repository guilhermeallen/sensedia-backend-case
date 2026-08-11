# Proposal: Fix POST /clientes Returning 500 on Name Validation Error

## Why
The `POST /clientes` endpoint currently returns HTTP 500 (Internal Server Error) when client name contains digits, a validation failure. The backend should return HTTP 400 (Bad Request) with a descriptive error message, following HTTP and REST conventions where client errors are 4xx, not 5xx.

## What Changes
- **Fix:** Change name validation error from `RuntimeError` (uncaught, becomes 500) to `HTTPException` with status 400
- **Consistency:** Apply the same error handling pattern as existing duplicate-check validations (CPF, email)
- **Error messaging:** Provide clear, actionable error details in the response

## Capabilities

### New Capabilities
- `cliente-creation-validation` — standardized error handling for client creation validation failures

### Modified Capabilities
- None (no existing capability changes; this is a defect fix)

## Impact
- **Code affected:** `app/services/cliente_service.py` (the `criar_cliente` method)
- **APIs affected:** `POST /clientes` endpoint response when name contains digits
- **Client impact:** API clients will receive proper 400 status and structured error message instead of 500
- **No database schema changes, no migrations, no new dependencies**

---

## Acceptance Criteria Met
- ✓ POST /clientes returns 400 instead of 500 when validation fails
- ✓ Error response includes descriptive message about the validation failure
- ✓ Behavior is consistent with other validation errors in the same service
