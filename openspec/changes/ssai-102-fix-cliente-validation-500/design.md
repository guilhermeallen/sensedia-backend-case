# Design: Client Creation Validation Error Handling

## Context
The `POST /clientes` endpoint in `app/services/cliente_service.py` currently enforces a rule: client names cannot contain digits. When a name contains digits, the code raises a bare `RuntimeError`, which is uncaught by FastAPI and escapes as an HTTP 500 response.

Two neighbouring validation checks in the same method (duplicate CPF, duplicate email) correctly raise `HTTPException` with HTTP 400 status. This inconsistency causes the digit-check validation to become an "internal server error" from the client's perspective, violating REST conventions.

**Current code (lines 12–16):**
```python
if re.search(r'\d', dados_cliente.nome):
    raise RuntimeError(
        f"Não é possível cadastrar o cliente '{dados_cliente.nome}': "
        f"nome contém número, indicando cadastro potencialmente inconsistente."
    )
```

The error message is clear and informative; only the exception type is wrong.

## Goals
1. Fix HTTP status code: 500 → 400 for name validation failures
2. Maintain consistent error handling across all client creation validations
3. Ensure error messages are descriptive and client-friendly

## Non-Goals
- Change the validation rule itself (whether digits are allowed) in this change
- Add validation to the `atualizar_cliente` method (a separate concern)
- Introduce new dependencies or middleware
- Change database schema

## Decisions

### Decision 1: Use HTTPException with status 400 for name validation
**Chosen:** Raise `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=<message>)` instead of `RuntimeError`.

**Rationale:**
- FastAPI automatically serializes `HTTPException` to JSON with the `detail` field
- Status 400 is semantically correct for client-supplied validation failures
- Matches the pattern used for duplicate checks 2 lines below in the same method
- The error message is already well-written; no change needed, only the exception type

**Alternatives considered:**
- Keep `RuntimeError` and add a global exception handler: Would work, but violates the codebase's own convention (duplicate checks use `HTTPException` directly in the service layer)
- Add validation to the request schema: Would prevent bad data earlier, but the validation is business logic (what names are acceptable), not input schema validation; belongs in the service

### Decision 2: Import `status` from fastapi for clarity
**Chosen:** Use `status.HTTP_400_BAD_REQUEST` constant for the HTTP status code.

**Rationale:**
- The codebase already imports and uses this pattern (seen in the duplicate-check validations)
- More readable than magic number 400
- Consistent with the existing codebase style

## Risks & Trade-offs

| Risk | Mitigation |
|---|---|
| Breaking change for any client expecting 500 | Low risk; a 500 indicates a bug, not documented contract. Clients should not rely on 500. If any client has a workaround for this specific 500, they should remove it and treat 400 as the proper error. |
| Name validation rule may change in the future | This change is independent of the rule itself; if the rule is later removed or relaxed, the HTTP status fix remains valid. |
| Inconsistency with `atualizar_cliente` (doesn't validate names) | Documented in this design; not a blocker for this fix, but a separate issue for future refinement. |

## Open Questions

### Question 1: Should client names be allowed to contain digits?
**Current evidence:**
- The digit-check rule exists only in `criar_cliente`, not in `atualizar_cliente`
- The database schema has no constraint (just `String(100)`)
- The business context is not explained in code comments or documentation

**Options:**
- **Option A (Keep the rule):** Assume the rule is intentional; apply it consistently to both create and update operations. Requires changes to `atualizar_cliente` as well.
- **Option B (Remove the rule):** Allow digits in names everywhere; the rule may have been overly strict. Simpler implementation, allows more name variations.
- **Option C (Clarify and decide):** Business/product team decides: is this a data-quality requirement, a user-facing constraint, or an oversight?

**Recommendation:**
Option A or B are both defensible. Option C (defer to product team) is safest. For **this change**, apply the fix (500 → 400) regardless of the rule's ultimate fate. The HTTP status defect is orthogonal to whether the rule should exist.

**Why it's a product decision, not technical:**
- No code comment explains why digits are forbidden
- The rule is inconsistently applied (create but not update)
- Removing a validation is a business policy change, not a code fix
- The alert and the card focus on the HTTP status, not on whether the rule should exist

---

## Implementation Notes
- No migrations or schema changes required
- No new dependencies
- Validation remains in the service layer (as it should be)
- Error message text does not change; only the exception type and HTTP status
