# Design: Client Name Validation Error Handling

## Context

The Sensedia API backend validates client names during creation and update operations. Currently, a name containing digits triggers a `RuntimeError` in `ClienteService.criar_cliente()` (line 13), which the global exception handler catches and converts to HTTP 500. However, sibling validation rules in the same function (CPF duplication, email duplication) correctly raise `HTTPException` with HTTP 400, establishing a clear convention within the file.

The issue manifests in QA when clients submit names with digits (e.g., "João da Si4lva"), causing the endpoint to return an ambiguous 500 error instead of a semantically correct client-side error. The backend logs contain clear evidence: `RuntimeError` raised by the name validation rule, not by any other component.

## Goals
1. Fix the error code — Replace `RuntimeError` with an appropriate HTTP exception
2. Maintain consistency — Ensure all validation errors follow the same handling pattern across create and update operations
3. Preserve the validation rule — Keep the "no digits in names" constraint; only fix how it fails
4. Improve observability — Return explicit, actionable error messages instead of generic 500 responses

## Decisions

### Decision 1: Use HTTP 422 for Name Validation
**Chosen:** HTTP 422 (Unprocessable Entity)
**Rationale:** Indicates semantic validation failure. FastAPI/Pydantic convention. Distinguishes semantic validation from resource-level validation.

### Decision 2: Apply Name Validation to Both Create and Update
**Chosen:** Add name validation to `atualizar_cliente()` method
**Rationale:** Consistency. Prevents a name valid in storage but invalid via API.

### Decision 3: Error Detail Message
**Chosen:** "Nome inválido: não é permitido incluir números"
**Rationale:** Clear, actionable, matches codebase language (Portuguese).

## Open Questions

### Question 1: Should Names with Digits Be Allowed at All?

**Option A. Keep the rule (RECOMMENDATION)**
- Keep current validation, fix error type only
- Conservative approach
- No evidence in code suggests rule should be removed

**Option B. Remove the rule entirely**
- Align with card recommendation
- Unknown why rule exists originally
- Wider blast radius

**Recommendation:** Option A. If the rule itself should change, that is a separate product decision.

**This will be settled by APPROVAL 1 (spec review).**
