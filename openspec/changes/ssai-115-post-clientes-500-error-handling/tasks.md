# Implementation Tasks: Client Creation Error Handling Consistency

## 1. Fix Error Handling

- [ ] 1.1 Update `app/services/cliente_service.py::ClienteService.criar_cliente` to raise `HTTPException(status_code=400, detail=...)` instead of `RuntimeError` when the name contains digits
- [ ] 1.2 Verify the exception message is clear and consistent with other validation messages in the method
- [ ] 1.3 Test manually using Postman collection: send POST /clientes with a name containing a digit (e.g., "João da Si4lva"), confirm HTTP 400 response

## 2. Verification

- [ ] 2.1 Confirm no other RuntimeError raises exist in the ClienteService
- [ ] 2.2 Verify the change does not affect other endpoints (GET, PUT, PATCH, DELETE)
- [ ] 2.3 Document in the PR that the fix is error-type correction, no logic change
