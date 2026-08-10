# Design — SSAI-94: POST /clientes Error Handling

## Context
The `POST /clientes` endpoint currently rejects client names containing numeric digits and returns HTTP 500 (Internal Server Error) because the validation error is raised as a bare `RuntimeError`. This violates the endpoint's established error-handling pattern, where validation failures (duplicate CPF, duplicate email) correctly signal client errors with HTTP 400.

**Current Code** (`app/services/cliente_service.py`):
```python
def criar_cliente(self, dados_cliente: ClienteCreate):
    import re
    if re.search(r'\d', dados_cliente.nome):
        raise RuntimeError(...)  # ← Uncaught, becomes 500
    
    if self.repository.buscar_por_cpf(dados_cliente.cpf):
        raise HTTPException(status_code=400, ...)  # ← Correct
    
    if self.repository.buscar_por_email(dados_cliente.email):
        raise HTTPException(status_code=400, ...)  # ← Correct
```

## Goals
1. **Primary:** Fix the error-handling inconsistency by raising `HTTPException` with HTTP 400 instead of `RuntimeError`
2. **Secondary:** Ensure all client-registration validation rules return appropriate 4xx errors

## Non-Goals
- Changing the business logic of validation (i.e., what the service accepts or rejects)
- Altering the behavior of duplicate CPF or email validation
- Adding new validation rules

## Decisions

### Decision 1: Error Handling — HTTPException vs RuntimeError
**Choice:** Raise `HTTPException(status_code=400, detail="...")` for name validation failures.

**Rationale:**
- Consistency: CPF and email validation already use this pattern in the same method
- Correctness: A client-supplied invalid name is a 4xx (client error), not a 5xx (server error)
- Observability: FastAPI automatically formats HTTPException responses into proper JSON error bodies

**Alternatives:**
- **Option A (rejected):** Add a global exception handler for RuntimeError in `app/main.py`. This would mask the inconsistency and create a non-obvious coupling between the service layer and the HTTP layer. The service should raise HTTP-aware exceptions directly.
- **Option B (rejected):** Create a custom validation exception hierarchy. Over-engineering for a single validation rule; HTTPException is already available and follows FastAPI conventions.

### Decision 2: Name Validation Rule — Keep or Remove?
**Choice:** Keep the "no digits in names" rule as-is; only fix the error handling.

**Rationale:**
- The rule exists in the code for a reason (likely a business requirement)
- Removing validation is a broader change that requires product/business confirmation
- The bug is in the error-handling pathway, not the validation itself
- Maintaining the rule with correct error signaling is the safest fix

**Alternatives:**
- **Option A (for spec review):** Remove the digit-validation rule entirely, allowing names with numbers (e.g., "João da Silva 2"). This aligns with the monitoring alert's recommendation. *Trade-off:* Assumes the rule was unintentional or can be safely dropped; risks breaking a business requirement if that assumption is wrong.
- **Option B (for spec review):** Make the digit check configurable or parameterized by business logic. *Trade-off:* Adds complexity without clarifying the rule's intent.

---

## Open Questions

### Q1: Should the "no digits in names" validation rule be kept, modified, or removed?
**Evidence:**
- The rule currently exists and is enforced in production code
- The monitoring alert recommends relaxing or removing the rule (allows names with digits)
- No code comments or test cases explain the business intent behind the rule
- The repository has no documentation (e.g., CONTRIBUTING.md, design notes) stating why names cannot contain digits

**Options:**
1. **Keep the rule** (recommended): Maintain the current validation logic; only fix error handling (HTTP 400 instead of 500). Safest option; requires no product decision.
2. **Remove the rule entirely**: Allow all client names, even those with digits. Aligns with the alert's recommendation; requires confirming this is intentional and does not violate a business rule (e.g., data integrity, compliance, external system expectations).
3. **Make the rule configurable**: Add a setting to toggle digit validation. Adds implementation complexity without answering the underlying question of what the rule should be.

**Recommendation:** Choose Option 1 (keep the rule) for this change. If the product team wants to relax the validation, that is a separate business decision to be made and tracked separately. This change focuses on the confirmed technical defect: error handling inconsistency.

---

## Risks / Trade-offs

| Risk | Mitigation |
|------|-----------|
| **No test suite exists for validation** — Changes cannot be verified against a test suite before deployment | Add tests as part of this change covering all three validation paths (name, CPF, email) to ensure consistent behavior going forward. Propose pytest as a baseline if the project adopts it. |
| **Database URL not available in sandbox** — Live integration tests cannot run locally | Tests will be unit-level (mocking the repository layer) to verify error codes. Integration tests should run in CI against a test database. |
| **Change depends on understanding the digit-validation rule's intent** — If we keep the rule and it is later deemed incorrect, the change will need adjustment | The decision is documented here. If product feedback requires removing the rule, that is a separate follow-up; this change captures the minimum fix for the confirmed defect. |

---

## Harness Constraints
- **Python:** 3.11.14 (sandbox) vs 3.x (declared in README)
- **Test command:** None exists yet; change will introduce tests or propose a baseline
- **Linters:** None declared; change will run existing lint (if any) or propose a baseline
- **Database:** PostgreSQL required; not available in sandbox; tests will mock the repository layer
