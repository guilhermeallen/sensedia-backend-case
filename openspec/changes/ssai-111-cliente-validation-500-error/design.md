# Design: Client Validation Error Response

## Context

The `POST /clientes` endpoint is returning HTTP 500 when client names contain digits. This was reported via an automated alert monitoring HTTP response status codes in the QA environment (SSAI-111 FA Alert).

**Current behavior:**
- Client name validation (checking for digits) exists and is intentional
- The validation raises an unhandled `RuntimeError` in `app/services/cliente_service.py:criar_cliente()`
- This `RuntimeError` propagates to the `generic_exception_handler()` in `app/main.py`, which catches all unhandled exceptions and returns HTTP 500
- Sibling business rules in the same method (CPF uniqueness, email uniqueness) correctly raise `HTTPException` with HTTP 400

**Root cause:** inconsistent error handling. Three sibling validation rules exist in the same method; two raise `HTTPException` (4xx), one raises bare `RuntimeError` (5xx).

## Goals

1. **Fix the HTTP status code:** validation errors must return 400, not 500
2. **Improve observability:** errors logged during request handling should classify validation failures separately from unhandled exceptions
3. **Maintain the business rule:** continue rejecting names with digits; this is not a product decision, it is an existing constraint
4. **Consistency:** all validation failures in `criar_cliente()` must follow the same error-handling pattern

## Non-Goals

- Decide whether the "no digits in name" rule should exist — it is an existing requirement; this change only fixes how it is reported
- Add new validations
- Change the set of fields validated
- Modify the update endpoint (`atualizar_cliente`) unless the same defect appears there

## Decisions

### Decision 1: Raise HTTPException with status 400 instead of RuntimeError
**Chosen:** Raise `HTTPException(status_code=400, detail="message")`

**Rationale:** 
- Matches the pattern used by the other two business rules in the same method
- HTTPException is caught by FastAPI's `http_exception_handler`, which logs at WARNING level (appropriate for invalid input)
- status 400 correctly signals that the client request was malformed, not a server error

**Alternatives considered:**
1. Add a custom exception handler for `RuntimeError` in `app/main.py` that returns 400 — would work but leaves the inconsistency in the code layer; a future developer might not realize why `RuntimeError` returns 4xx here but 5xx elsewhere
2. Keep `RuntimeError` and add Pydantic field validation to `ClienteCreate` — would move validation to the schema layer, but loses the ability to provide a detailed business message; Pydantic validators are designed for type/format validation, not business rules

### Decision 2: Error message clarity
**Chosen:** Detail message states the business rule plainly: "Não é possível cadastrar o cliente: nome contém número"

**Rationale:**
- Aligns with the existing message in the RuntimeError (shown in traces)
- Explains both the rejection and the reason (names must not contain digits)
- Consistent with detail messages from other validations in the method

## Risks / Trade-offs

[Risk] **Breaking change for clients:** Any client code that was catching HTTP 500 from this endpoint and treating it as a server error (e.g., implementing retry logic, incident alerting) will now receive 400 and may behave differently.

→ **Mitigation:** This is a bug fix, not a feature change. The 500 response was incorrect; fixing it is a correctness issue. Clients should have been treating invalid input as 4xx, not 5xx. Upgrade notes can document this as a bug fix.

[Risk] **Overlooking similar defects:** The same pattern (bare RuntimeError in validation logic) might exist in other service methods.

→ **Mitigation:** Not addressed in this change; a future code review or linter rule could catch these. This change focuses on the `criar_cliente` method that triggered the alert.

## Open Questions

None. The validation rule itself is not questioned by this change; it is an existing business constraint. The change is purely corrective.
