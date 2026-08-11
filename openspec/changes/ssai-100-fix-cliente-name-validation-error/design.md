# Design: Client Name Validation Error Handling

## Context

The `ClienteService.criar_cliente()` method enforces a business rule that client names must not contain numeric digits. When a name violates this rule, the service raises a bare `RuntimeError`, which is not caught by any handler in the HTTP exception-handling middleware. The error propagates up as an unhandled exception, resulting in an HTTP 500 response from the FastAPI generic exception handler in `app/main.py`.

In contrast, two other validation rules in the same method (CPF duplicate check, email duplicate check) correctly raise `HTTPException` with status code 400, signaling a client error.

This inconsistency is the root cause of SSAI-100: an invalid client name request generates a 500 instead of the expected 400.

## Goals

- **Primary:** Return HTTP 400 (Bad Request) with a clear error message when a client name contains digits, aligning with the existing error-handling pattern.
- **Secondary:** Maintain the existing validation rule (reject names with digits) unless the spec-review gate decides otherwise.

## Non-Goals

- Change the underlying validation logic (whether digits should be allowed).
- Modify other validation rules or error-handling patterns in the codebase.
- Add logging, metrics, or other observability beyond what exists in the generic exception handler.

## Decisions

### Decision 1: Error Response Status Code

**Choice:** HTTP 400 (Bad Request).

**Rationale:**
- The error is caused by invalid client input (a name with digits), not a server malfunction.
- HTTP 400 is the standard for client-side validation failures.
- The two sibling validation rules (CPF/email) use 400 for the same class of error.

**Alternatives considered:**
- HTTP 422 (Unprocessable Entity): Also valid for semantic/business-logic validation errors. However, 400 is more widely supported and consistent with the existing codebase.

### Decision 2: Exception Type

**Choice:** `HTTPException(status_code=400, detail="...")` from FastAPI.

**Rationale:**
- FastAPI's `HTTPException` is caught by the framework's built-in exception handler, which correctly returns the status code and detail message.
- The two sibling rules use the same pattern, confirming it is the codebase convention.
- No need to create custom exception classes or add new handlers.

**Alternatives considered:**
- Creating a custom `ClienteValidationError` exception and adding a dedicated handler: overkill for a single validation rule; the pattern already exists and works.

### Decision 3: Error Message Content

**Choice:** Reuse the existing message template but wrap it in `HTTPException`.

**Rationale:**
- The current message is clear and actionable: "Não é possível cadastrar o cliente '<name>': nome contém número, indicando cadastro potencialmente inconsistente."
- No localization or message change is required; only the exception type needs to change.

## Risks & Trade-offs

### Risk 1: Validation Rule Itself May Be Overly Strict

**Evidence:** The monitoring alert recommendation suggests allowing numbers or normalizing input. However, the code shows the rule is intentional (not a typo), and no business requirement in the card argues for removing it.

**Mitigation:** Document this as an open question for the spec-review gate (below). The fix itself (error status code) is independent of whether the rule should exist.

### Risk 2: Missing Test Coverage

**Evidence:** The harness report shows zero tests exist in the project. This change will be untested by the existing suite (because none exists).

**Mitigation:** The change introduces test case(s) as part of the implementation (see tasks.md). A test will verify the error response status and message.

## Open Questions

### Question 1: Should Client Names With Digits Be Rejected?

**Context:** The validation rule rejects any name containing digits (0-9). Real-world names may include digits (e.g., "João 2º Silva"), though such cases are rare in Portuguese naming conventions.

**Options:**

| Option | Pros | Cons |
|---|---|---|
| **Keep the rule (Recommendation)** | Existing rule, narrowest fix, lower risk of unintended side effects. | Excludes edge cases with valid digits. |
| **Remove the rule** | Broader acceptance of valid input. | Wider blast radius: updates validation, tests, documentation. Requires clarity on why it was added. |
| **Modify the rule (e.g., allow suffix digits only)** | Compromise between safety and flexibility. | More complex regex; needs clear definition of allowed patterns. |

**Recommendation:** Keep the rule as-is. The error-handling fix (this change) is separate from the business decision of whether digits should be allowed. If the rule should be relaxed, that is a distinct product decision for a follow-up issue.

**Decision:** Deferred to spec-review gate (APPROVAL 1).

---

## Summary

This change corrects an error-handling defect: wrapping a validation exception in `HTTPException(400, ...)` instead of letting a bare `RuntimeError` escape as a 500. The fix is small, isolated, and follows the existing convention in the codebase. One open question (whether the validation rule itself should survive) is documented for the gate to decide; it does not block the implementation.
