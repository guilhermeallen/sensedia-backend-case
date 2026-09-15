# Implementation Tasks

## 1. Fix Error Handling

- [x] 1.1 Update `app/services/cliente_service.py` — replace `RuntimeError` with `HTTPException(status_code=422)` in name validation
- [x] 1.2 Verify the change compiles and imports are correct

## 2. Testing

- [x] 2.1 Add unit test for valid client creation (name without digits)
- [x] 2.2 Add unit test for invalid client creation (name with digits) — verify HTTP 422 response
- [x] 2.3 Add unit test for error response JSON structure
- [x] 2.4 Run all tests locally and confirm they pass

## 3. Validation

- [x] 3.1 Run lint check (setup baseline if needed)
- [x] 3.2 Run type-check if available (setup baseline if needed)
- [x] 3.3 Verify no regressions in other validations (CPF/email checks still return 400)

## 4. Documentation

- [x] 4.1 Update API documentation or error response specs if applicable
- [x] 4.2 Confirm the change is reflected in generated OpenAPI schema (FastAPI auto-generates this)
