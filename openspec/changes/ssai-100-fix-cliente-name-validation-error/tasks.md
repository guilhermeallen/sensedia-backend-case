# Implementation Tasks

## 1. Code Changes

- [ ] 1.1 Modify `ClienteService.criar_cliente()` to wrap the name validation exception in `HTTPException(status_code=400, detail="...")`
- [ ] 1.2 Verify the modified service imports FastAPI's `HTTPException` and `status`

## 2. Testing

- [ ] 2.1 Create a test case verifying that a POST request with a name containing digits returns HTTP 400
- [ ] 2.2 Create a test case verifying that the error response detail message is correct
- [ ] 2.3 Create a test case verifying that names without digits are still accepted (regression test)
- [ ] 2.4 Run all new tests locally and confirm they pass

## 3. Validation & Cleanup

- [ ] 3.1 Verify no syntax errors or import issues in the modified service
- [ ] 3.2 Confirm `git status` shows only expected changes (no stray files or accidental modifications)
- [ ] 3.3 Review the diff to ensure the change aligns with the spec

## 4. Documentation (Optional)

- [ ] 4.1 If a README or API docs exist describing error codes, verify they are consistent with the change
