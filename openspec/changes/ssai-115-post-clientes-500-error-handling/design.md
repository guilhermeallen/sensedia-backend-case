# Design: Client Creation Error Handling Consistency

## Context
The backend service receives HTTP 500 errors on POST /clientes when the client name contains digits. Investigation reveals that:
1. The validation rule exists and correctly identifies invalid names (e.g., "João da Si4lva")
2. The rule is enforced in `ClienteService.criar_cliente` via `raise RuntimeError(...)`
3. Two sibling validation rules in the same method correctly signal failures with `HTTPException(status_code=400, ...)`
4. The RuntimeError is not caught by the global exception handler, bubbles up as a 500

This is a defect in error consistency, not a question about whether the rule should exist.

## Goals
- Fix HTTP 500 responses by raising the correct exception type
- Align all validation failures in client creation with HTTP 400 status
- Keep the validation logic intact (no change to what is accepted/rejected)

## Non-Goals
- Remove or modify the digit-in-name validation rule itself
- Change validation logic or business rules
- Refactor the service layer beyond what's needed for this fix

## Decisions

### Decision 1: Use HTTPException instead of RuntimeError
**Chosen:** Replace `RuntimeError` with `HTTPException(status_code=400, detail=...)`

**Rationale:** The existing code already demonstrates the correct pattern in the same method:
```python
if self.repository.buscar_por_cpf(dados_cliente.cpf):
    raise HTTPException(status_code=400, detail="Já existe um cliente cadastrado com este CPF.")
```
Consistency with existing patterns is the highest-priority principle in this codebase.

**Alternatives considered:**
1. Wrap the RuntimeError in a try-except at the router level — adds unnecessary complexity; the service should handle its own errors
2. Add RuntimeError to the global exception handler — incorrect because RuntimeError is too broad; it could mask bugs elsewhere
3. Create a custom exception class — over-engineering; HTTPException is the standard in FastAPI and already used here

## Risks / Trade-offs
- **Risk:** No test suite exists to verify the change. **Mitigation:** The fix is localized to one line, manual testing with the Postman collection can verify the status code change.
- **Risk:** Changing HTTP status from 500 to 400 may affect external monitoring/alerting that filters on status codes. **Mitigation:** This is a correction to semantically correct behavior; downstream systems expecting 500 for validation errors are incorrectly configured.

## Open Questions
None. The fix is straightforward error-type correction against the existing pattern.
