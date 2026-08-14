# Implementation Tasks

## 1. Service Layer Changes

- [ ] 1.1 Extract name validation into a private `_validar_nome()` method in `ClienteService`
- [ ] 1.2 Update `criar_cliente()` to call `_validar_nome()` and raise `HTTPException(status_code=400)` instead of `RuntimeError`
- [ ] 1.3 Update `atualizar_cliente()` to call `_validar_nome()` for the name field if present
- [ ] 1.4 Ensure error messages are consistent across all validation failures

## 2. Testing

- [ ] 2.1 Create unit tests for `ClienteService._validar_nome()` covering valid names and names with digits
- [ ] 2.2 Create unit tests for `ClienteService.criar_cliente()` covering the error case (name with digits)
- [ ] 2.3 Create unit tests for `ClienteService.atualizar_cliente()` covering the error case (name with digits in update)
- [ ] 2.4 Create integration tests for `POST /api/v1/clientes` to verify HTTP 400 response on name validation failure
- [ ] 2.5 Create integration tests for `PUT /api/v1/clientes/{id}` to verify HTTP 400 response on name validation failure
- [ ] 2.6 Create integration tests for `PATCH /api/v1/clientes/{id}` to verify HTTP 400 response on name validation failure
- [ ] 2.7 Verify all existing tests still pass after the changes

## 3. Code Quality

- [ ] 3.1 Format code with project standards (Python style)
- [ ] 3.2 No linting errors
- [ ] 3.3 Type hints are correct
- [ ] 3.4 Error messages are clear and user-friendly

## 4. Verification

- [ ] 4.1 Verify that POST /clientes with a name containing digits returns HTTP 400 (not 500)
- [ ] 4.2 Verify that PUT /clientes/{id} with a name containing digits returns HTTP 400
- [ ] 4.3 Verify that PATCH /clientes/{id} with a name containing digits returns HTTP 400
- [ ] 4.4 Verify that successful create/update operations (valid names) still work correctly
- [ ] 4.5 Verify that other validation errors (duplicate CPF, duplicate email) still return HTTP 400 as expected
- [ ] 4.6 Verify that unhandled exceptions in other code paths still return HTTP 500
