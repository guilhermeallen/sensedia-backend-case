# Implementation Tasks

## 1. Fix Name Validation Error Handling

- [x] 1.1 Modify `app/services/cliente_service.py`: Change `RuntimeError` to `HTTPException` with status 400 in `criar_cliente` method
- [x] 1.2 Verify import of `status` from `fastapi` is present at the top of the file
- [x] 1.3 Test the error response format manually (POST /clientes with a name containing digits, confirm 400 response with detail field)

## 2. Verify Consistency

- [x] 2.1 Confirm all three validation failures in `criar_cliente` follow the same `HTTPException` pattern:
  - Name contains digits
  - CPF already exists
  - Email already exists
- [x] 2.2 Check that error messages are clear and consistent in tone

## 3. Code Review

- [x] 3.1 Self-review the diff: is the change minimal and focused on the HTTP status defect?
- [x] 3.2 Confirm no other files are touched (no model, schema, or router changes needed)

## 4. Documentation (if applicable)

- [x] 4.1 Verify existing API documentation (README, Postman collection) does not need updating
- [x] 4.2 Note: The API contract change (500 → 400) should be mentioned in release notes if the project maintains a CHANGELOG
