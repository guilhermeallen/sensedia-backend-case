# Specification: Client Creation Validation Error Handling

## ADDED Requirements

### Requirement: Validation failures SHALL return HTTP 400
The system SHALL return HTTP 400 (Bad Request) with a descriptive error message when client creation validation fails, not HTTP 500 (Internal Server Error).

#### Scenario: Name contains digits
- **WHEN** user attempts to create a client with a name containing digits (e.g., `"João Silva 4"`)
- **THEN** the system SHALL return HTTP 400 with error detail: `"Não é possível cadastrar o cliente '[nome]': nome contém número, indicando cadastro potencialmente inconsistente."`

#### Scenario: CPF already registered
- **WHEN** user attempts to create a client with a CPF already in use
- **THEN** the system SHALL return HTTP 400 with error detail: `"Já existe um cliente cadastrado com este CPF."`

#### Scenario: Email already registered
- **WHEN** user attempts to create a client with an email already in use
- **THEN** the system SHALL return HTTP 400 with error detail: `"Já existe um cliente cadastrado com este E-mail."`

### Requirement: Error responses SHALL be consistent in format
The system SHALL return all validation failures in the same HTTP format, following FastAPI's HTTPException pattern with a structured `detail` field.

#### Scenario: Error response format
- **WHEN** a validation error occurs
- **THEN** the HTTP response body SHALL contain a JSON object with a `detail` field containing the error message
- **AND** the response SHALL NOT contain a raw Python traceback

### Requirement: Validation SHALL be applied at service layer only
The business logic validation for client names SHALL occur in `ClienteService.criar_cliente()`, not in request handlers or schemas.

#### Scenario: Service-layer validation
- **WHEN** `ClienteService.criar_cliente()` is called with invalid data
- **THEN** the service SHALL raise `HTTPException` with the appropriate status and detail
- **AND** the router handler SHALL not catch or re-interpret the exception
