# Tasks: Fix POST /clientes Validation Error Handling

## 1. Core Implementation

- [ ] 1.1 Modify `app/services/cliente_service.py` to raise `HTTPException(status_code=400)` instead of `RuntimeError` for name validation
- [ ] 1.2 Ensure the error message is user-friendly and consistent with other validation errors
- [ ] 1.3 Verify the change compiles and has no syntax errors

## 2. Testing

- [ ] 2.1 Write test for invalid name with digits — expects HTTP 400 with validation message
- [ ] 2.2 Write test for valid name without digits — expects HTTP 201 and successful creation
- [ ] 2.3 Write test to confirm error response format matches other validation errors (duplicate CPF, duplicate email)
- [ ] 2.4 Run all tests and confirm they pass

## 3. Verification

- [ ] 3.1 Manually test POST /clientes with a name containing digits (should return 400, not 500)
- [ ] 3.2 Manually test POST /clientes with a valid name (should return 201)
- [ ] 3.3 Confirm the error response body includes a clear detail message
- [ ] 3.4 Verify no unrelated tests are broken by the change

## 4. Code Quality

- [ ] 4.1 Ensure the code follows the existing style and patterns in `app/services/`
- [ ] 4.2 Add inline documentation if the validation rule's intent is unclear to future maintainers
- [ ] 4.3 Check for any similar RuntimeError patterns elsewhere in the codebase that should also be fixed

## 5. Documentation

- [ ] 5.1 Update README.md or API documentation if customer name validation is documented
- [ ] 5.2 Add a comment to the validation rule explaining why digits are rejected (if the reason is known)

## 6. Commit and Push

- [ ] 6.1 Commit changes with a clear message
- [ ] 6.2 Push to the feature branch
- [ ] 6.3 Confirm the branch is pushed to the remote repository
