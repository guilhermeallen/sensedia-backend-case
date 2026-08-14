# Design: Client Creation Error Handling Fix

## Context
The alert reported that `POST /clientes` was returning HTTP 500 when a client's name contained digits. Investigation revealed:
- The gateway (Sensedia API Manager) correctly forwarded the request to the backend
- The backend (sensedia-api-backend) returned the 500 error
- Root cause: `app/services/cliente_service.py:12` raises `RuntimeError` for names with digits

The `RuntimeError` is unhandled by FastAPI's exception handlers, so it falls through to the generic `@app.exception_handler(Exception)` in `app/main.py:62`, which logs it and returns a 500 response. This violates the API's own error-handling convention: other validation failures (duplicate CPF, duplicate email) raise `HTTPException(status_code=400)`.

## Goals
1. Fix the unhandled exception so that name validation failures return HTTP 400 (not 500)
2. Align the name validation error handling with the existing pattern for other business rules
3. Prevent similar unhandled exceptions in update operations (PUT, PATCH)

## Non-Goals
- Changing the validation logic itself (whether names should allow digits) — this is an open product decision
- Adding new validation rules beyond the digit check
- Refactoring the service layer or repository pattern

## Decisions

### Decision 1: The "no digits in name" rule — keep or remove?
**Status:** Open product decision for spec review

The digit-validation rule exists in the code but has no documented rationale. The alert recommendation suggests removing it; however, removing a business rule is a product decision, not an engineering fix.

**Recommendation:** Keep the rule because (a) it's currently in production, (b) removing it should be a separate product decision from fixing the error-handling defect, (c) the fix (HTTP 400 instead of 500) is still an improvement regardless.

### Decision 2: Should update operations (PUT, PATCH) also validate names?
**Status:** Open decision with a recommendation

**Recommendation:** Option 2 (apply validation in both). The name digit rule is a business constraint; it should be enforced everywhere the name is modified.

## Risks and Trade-offs

| Risk | Mitigation |
|------|-----------|
| **Risk:** Changing error response status breaks existing API consumers expecting 500 | **Mitigation:** 500 responses for validation errors are bad practice. This is a defect fix. |
| **Risk:** The update endpoint (PUT, PATCH) might be forgotten | **Mitigation:** Extract validation into a shared method, call from both create and update. |
| **Risk:** Tests don't exist; regression is possible | **Mitigation:** Spec includes test scenarios; implementation will add unit and integration tests. |

## Implementation Strategy
1. Create a private `_validar_nome()` method in `ClienteService` to check for digits
2. Modify `criar_cliente()` to call `_validar_nome()` and raise `HTTPException(status_code=400)` on failure
3. Modify `atualizar_cliente()` to call `_validar_nome()` if the name field is being updated
4. Add unit tests for both validation success and failure paths
5. Add integration tests for the API endpoints to verify HTTP 400 responses
