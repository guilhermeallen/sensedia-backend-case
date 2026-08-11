# Tasks: Client Name Validation Error Handling

## 1. Fix Client Creation Name Validation

- [ ] 1.1 Update `ClienteService.criar_cliente()` to raise `HTTPException` with status 422 instead of `RuntimeError`
- [ ] 1.2 Update error detail message to "Nome inválido: não é permitido incluir números"
- [ ] 1.3 Verify exception import (`from fastapi import HTTPException, status`) exists in the file

## 2. Add Client Update Name Validation

- [ ] 2.1 Add name validation check to `ClienteService.atualizar_cliente()` when name field is being updated
- [ ] 2.2 Raise `HTTPException` with status 422 and message "Nome inválido: não é permitido incluir números"
- [ ] 2.3 Ensure validation only applies if name field is actually being changed (check `if "nome" in dados_novos`)

## 3. Code Quality

- [ ] 3.1 Verify no other RuntimeError exceptions are raised in `ClienteService`
- [ ] 3.2 Ensure consistent error handling across all validation rules in both methods

## 4. Testing

- [ ] 4.1 Write test for POST /clientes with valid name (no digits) → HTTP 201
- [ ] 4.2 Write test for POST /clientes with invalid name (contains digit) → HTTP 422
- [ ] 4.3 Write test for PUT /clientes/{id} with valid name (no digits) → HTTP 200
- [ ] 4.4 Write test for PUT /clientes/{id} with invalid name (contains digit) → HTTP 422
- [ ] 4.5 Write test for PATCH /clientes/{id} with valid name update → HTTP 200
- [ ] 4.6 Write test for PATCH /clientes/{id} with invalid name update → HTTP 422
- [ ] 4.7 Write test confirming duplicate CPF still returns 400, not 422
- [ ] 4.8 Write test confirming duplicate email still returns 400, not 422
- [ ] 4.9 Write test confirming update without name field skips name validation
- [ ] 4.10 Run all tests and confirm they pass

## 5. Verification

- [ ] 5.1 Verify POST /clientes with "João da Si4lva" now returns 422 (previously 500)
- [ ] 5.2 Verify response body contains detail message "Nome inválido: não é permitido incluir números"
- [ ] 5.3 Verify POST /clientes with valid name still works (201)
- [ ] 5.4 Verify PUT and PATCH name updates are consistent with POST validation
- [ ] 5.5 Verify no regressions in CPF/email duplicate detection (still return 400)
