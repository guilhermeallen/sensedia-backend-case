# Proposal: Fix Cliente Validation Error Handling

## Why

POST /clientes returns HTTP 500 in QA when client name validation fails. The validation rule itself (reject names containing digits) is intentional, but it raises an unhandled `RuntimeError` instead of a proper HTTP 4xx response. This violates the API's own error convention where business-rule violations signal with `HTTPException` and 4xx status codes.

## What Changes

- **Fix**: Replace `RuntimeError` in cliente name validation with `HTTPException(status_code=422)` 
  - Exception type change: `RuntimeError` → `HTTPException`
  - HTTP status: 500 → 422 (Unprocessable Entity — semantically correct for validation failure)
  - Error is now caught by FastAPI's built-in exception handler and returns proper JSON response

- **Affected endpoint**: POST /clientes (and any retry attempts on the same operation)

## Capabilities

### New Capabilities
- None

### Modified Capabilities
- `cliente-validation` — error handling for cliente name validation is fixed

## Impact

- **Code modified**: `app/services/cliente_service.py` (1 line change)
- **API surface**: POST /clientes error response changes from 500 to 422
- **Affected systems**: Any client calling POST /clientes with invalid name; previously would receive 500, now will receive proper 422 error with description
- **Backward compatibility**: Clients expecting 500 on this validation will now see 422; this is an improvement (fixes the bug), not a breaking change in intended behavior
- **Test requirements**: Unit test for error response status code and message
- **Documentation**: Error response code documentation may need updating to reflect 422 instead of 500

## Acceptance Criteria Traceability

- "POST /clientes retornando 500" (title) → Fixed: now returns 422 for validation error
- "Backend rejects a name containing a digit" (analysis) → Kept: validation rule preserved
- "adjust validation to return proper HTTP status" (recommendation) → Implemented: 422 instead of 500
