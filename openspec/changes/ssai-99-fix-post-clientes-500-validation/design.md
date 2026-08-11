# Design: Fix POST /clientes Validation Error Handling

## Context
The customer registration endpoint (`POST /clientes`) returns HTTP 500 when input validation fails for a customer name containing digits. This is a defect in error handling: validation failures are user input errors (4xx), not server errors (5xx).

**Current state:**
- `app/services/cliente_service.py` line 10-14 raises `RuntimeError("Não é possível cadastrar o cliente '...'")` when `cliente.nome` contains a digit.
- This exception is not caught by the FastAPI `@app.exception_handler(HTTPException)` handler.
- The generic `@app.exception_handler(Exception)` handler catches it and returns HTTP 500 with "Erro interno do servidor".
- Sibling validation rules for duplicate CPF and email use `HTTPException(status_code=400)` consistently.

**Alert evidence:**
- QA environment saw 5+ requests triggering HTTP 500 on the same endpoint in a few seconds (2026-08-11 01:34:35-54Z).
- Gateway logs show the backend responded with 500, not a timeout or forwarding issue.

## Goals
1. **Correct error handling** — return HTTP 400 Bad Request for validation failures, not 500.
2. **Consistency** — align all validation failures in `ClienteService.criar_cliente()` to use `HTTPException(status_code=400)`.
3. **No behavior change** — the validation rule itself (reject names with digits) is unchanged unless the product team decides otherwise.

## Non-Goals
- Deciding whether the "no digits in name" rule should exist, be relaxed, or be removed — this is a product decision, deferred to spec review.
- Changing validation logic for CPF or email.
- Modifying the database schema or migration.

## Decisions

### Decision 1: Use HTTPException(status_code=400) for the name validation error
**Choice:** Raise `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="...")` instead of `RuntimeError`.

**Rationale:**
- FastAPI's exception handlers are designed to catch `HTTPException` and return the specified status code.
- Sibling validation rules (duplicate CPF, duplicate email) already use this pattern.
- Aligns with REST convention: validation failures are client errors (4xx), not server errors (5xx).
- Gives clients a consistent, machine-readable error response.

**Alternatives considered:**
- Use `HTTPException(status_code=422, ...)` (Unprocessable Entity) — also valid for validation failures; `400` is chosen because the other validation rules use `400`, prioritizing consistency over strict HTTP semantics.
- Create a custom exception and add a new exception handler — introduces unnecessary complexity for a single rule; HTTPException is sufficient.
- Catch the RuntimeError in the router and re-raise as HTTPException — works but leaves the service inconsistent; better to fix the source.

### Decision 2: Keep the validation rule itself unchanged
**Choice:** Do not remove, modify, or relax the "no digits in name" rule; change only the exception type.

**Rationale:**
- The card's recommendation to "adjust the validation" refers to the HTTP status code, not the rule's existence.
- The rule has business context ("indicando cadastro potencialmente inconsistente") but no explicit decision is visible in the code about whether it is intentional.
- Removing a rule is a wider blast radius than fixing an error type; a human decision is warranted.
- The spec captures this as an open question below.

## Risks / Trade-offs

### [Risk] Validation rule may be intentional or outdated
If the "no digits in name" rule exists for a specific reason (e.g., legacy system integration), removing it later could have unintended side effects. If it is legacy and should have been removed, the fix defers that decision.

**Mitigation:** Documented as an open question for the spec-review gate. Product team can decide at approval time.

### [Risk] Clients expecting 500 on any validation error
Unlikely but possible: downstream clients may have error handling that depends on receiving 500 for validation failures. This is poor practice (4xx is the correct response), so the risk is minimal. Documented for awareness.

**Mitigation:** Return 400 is correct per HTTP semantics and REST conventions. Any client code expecting 500 for validation should be updated.

## Open Questions

### Question 1: Should the "no digits in name" validation rule be kept?

The code contains a rule rejecting customer names with digits:
```python
if re.search(r'\d', dados_cliente.nome):
    raise RuntimeError("Não é possível cadastrar o cliente '...': nome contém número, ...")
```

The message suggests this is intentional ("indicando cadastro potencialmente inconsistente"), but the codebase does not explain *why* this rule exists — is it a business requirement, a legacy constraint, or an overly conservative check?

**Evidence:**
- Code: `app/services/cliente_service.py` lines 10-14 (exists and is consistent with the message)
- Alert recommendation: "ajustar o backend para retornar 400/422 para erros de validação" (fix the status code, not explicit about the rule itself)
- Naming convention: "João da Si4lva" is a valid name in Portuguese, so rejecting it is a constraint, not a natural language rule

**Options:**

| Option | Pros | Cons |
|--------|------|------|
| **Keep the rule** | Stable, no surprise side effects, conservative. If the rule is intentional, removing it breaks something unknown. | Limits customer names (not all countries accept digit-free names; some systems use "João 2" to distinguish duplicates). |
| **Remove the rule** | Card recommendation points toward flexibility. Better UX for edge cases. | If the rule is intentional (e.g., legacy system integration), removing it silently could break downstream logic. |
| **Relax the rule** (e.g., allow digits at the end or in a suffix) | Compromise: keep intent, allow more names. | Requires more detailed specification of what's allowed and what's not. |

**Recommendation:** Keep the rule as-is for now. The error handling fix (500 → 400) is the urgent issue. If the product team decides the rule should be relaxed or removed, that is a follow-up task (separate ticket). This approach is safer and lets the gate make an informed decision.

**For the spec-review gate (APPROVAL 1):**
- If you want to **keep the rule**: approve as-is. The fix changes only the HTTP status code.
- If you want to **remove or relax the rule**: request adjustments in the "Ajustar Spec" column and specify the new validation logic.

---

## Implementation Approach

1. Modify `app/services/cliente_service.py`:
   - Replace `raise RuntimeError(...)` with `raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=...)`.
   - Ensure the message is user-friendly and matches the style of other validation errors.

2. Verify:
   - POST /clientes with a name containing digits now returns 400 (testable in QA).
   - POST /clientes with a valid name still succeeds (201 Created).
   - The response body format matches other validation error responses.

3. Test coverage:
   - No existing test suite, so the change adds tests to verify the new behavior (see tasks.md).

## Open Blockers
(None — the fix is straightforward once the spec is approved)
