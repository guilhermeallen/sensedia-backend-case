# Tasks — SSAI-94: POST /clientes Error Handling

## 1. Fix error handling in ClienteService

- [ ] 1.1 Update `app/services/cliente_service.py::criar_cliente()` to raise `HTTPException(status_code=400)` instead of `RuntimeError` for name validation failures
- [ ] 1.2 Verify the error message is clear and follows the pattern of existing validation errors (CPF, email)
- [ ] 1.3 Check the updated method for syntax errors and import statements

## 2. Add unit tests for validation error handling

- [ ] 2.1 Create `tests/test_cliente_service.py` (or similar structure based on project conventions if it exists)
- [ ] 2.2 Write a test case for name validation with digits (should return 400, not 500)
- [ ] 2.3 Write a test case for name validation without digits (should succeed)
- [ ] 2.4 Write a test case for duplicate CPF validation (should return 400)
- [ ] 2.5 Write a test case for duplicate email validation (should return 400)
- [ ] 2.6 Ensure all test cases verify the correct HTTP status code and error message format

## 3. Lint and format

- [ ] 3.1 Run project lint/format tools (if any exist) on modified and new files
- [ ] 3.2 Fix any lint errors or style violations

## 4. Verify the fix

- [ ] 4.1 Manually test the endpoint with a name containing digits and verify it returns 400 (if live database available)
- [ ] 4.2 Run the new test suite and confirm all tests pass
- [ ] 4.3 Confirm no existing tests were broken by the change
