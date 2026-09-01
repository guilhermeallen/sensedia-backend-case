# Implementation Tasks

## 1. Fix validation error handling

- [ ] 1.1 Update `ClienteService.criar_cliente()` to raise `HTTPException(status_code=400, detail="...")` instead of `RuntimeError` when name contains digits
- [ ] 1.2 Verify the error message is clear and consistent with other validation messages in the method

## 2. Testing & Verification

- [ ] 2.1 Manually test the endpoint with a client name containing digits (e.g., "João3") and confirm HTTP 400 is returned (not 500)
- [ ] 2.2 Manually test the endpoint with a valid client name and confirm HTTP 201 is returned and client is created
- [ ] 2.3 Manually test duplicate email scenario and confirm HTTP 400 is still returned
- [ ] 2.4 Manually test duplicate CPF scenario and confirm HTTP 400 is still returned

## 3. Code Review

- [ ] 3.1 Confirm the change is minimal and focused (one method, one error handling fix)
- [ ] 3.2 Check that imports are correct (HTTPException, status from fastapi)
- [ ] 3.3 Verify logging behavior (exception handler in main.py will log at WARNING, not ERROR)
