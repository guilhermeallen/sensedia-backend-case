# Specification: Client Creation Error Handling

## ADDED Requirements

### Requirement: POST /clientes rejects names with digits via HTTP 400
The system SHALL return HTTP 400 (Bad Request) with a structured error message when a client creation request includes a name containing any digit character.

#### Scenario: Client name contains a digit
- **WHEN** `POST /api/v1/clientes` receives `{"nome": "João Silva 4", "email": "joao@example.com", "cpf": "12345678900"}`
- **THEN** the endpoint returns HTTP 400 with `{"detail": "Não é possível cadastrar o cliente 'João Silva 4': nome contém número, indicando cadastro potencialmente inconsistente."}`
- **AND** no client record is created in the database
- **AND** the error is properly logged

#### Scenario: Client name contains multiple digits
- **WHEN** `POST /api/v1/clientes` receives `{"nome": "Client 123", "email": "client@example.com", "cpf": "98765432100"}`
- **THEN** the endpoint returns HTTP 400 with a validation error message
- **AND** the request is rejected before any database write

#### Scenario: Valid client name without digits succeeds
- **WHEN** `POST /api/v1/clientes` receives `{"nome": "João Silva", "email": "joao@example.com", "cpf": "12345678900"}`
- **THEN** the endpoint returns HTTP 201 (Created) with the created client object
- **AND** the client is successfully stored in the database

### Requirement: Error response is consistent with other validation errors
The system SHALL use the same HTTP status code (400) and error response structure for the name digit validation as it does for duplicate CPF and duplicate email validation.

#### Scenario: CPF duplicate validation also returns 400
- **WHEN** attempting to create a client with a CPF that already exists
- **THEN** the endpoint returns HTTP 400 with `{"detail": "Já existe um cliente cadastrado com este CPF."}`

#### Scenario: Email duplicate validation also returns 400
- **WHEN** attempting to create a client with an email that already exists
- **THEN** the endpoint returns HTTP 400 with `{"detail": "Já existe um cliente cadastrado com este E-mail."}`

#### Scenario: All validation errors use HTTP 400 status
- **WHEN** any business rule validation fails in `POST /api/v1/clientes`
- **THEN** the response status code is always 400 (Bad Request), never 500

### Requirement: Validation is applied consistently across all client operations
The system SHALL apply the name digit validation to all client write operations (create and update).

#### Scenario: Update endpoint rejects names with digits
- **WHEN** `PUT /api/v1/clientes/{id}` receives a client update with `"nome": "João 5"`
- **THEN** the endpoint returns HTTP 400 with a validation error message

#### Scenario: Patch endpoint rejects names with digits
- **WHEN** `PATCH /api/v1/clientes/{id}` receives a client update with `"nome": "Silva 99"`
- **THEN** the endpoint returns HTTP 400 with a validation error message

### Requirement: Exception handling does not leak unhandled exceptions to clients
The system SHALL not return HTTP 500 for validation rule violations. All validation errors MUST be caught and converted to appropriate HTTP 4xx responses.

#### Scenario: No 500 on name digit validation
- **WHEN** `POST /api/v1/clientes` is called with a name containing digits
- **THEN** the response is HTTP 400 (not 500)
- **AND** the generic exception handler is not invoked

#### Scenario: Other exceptions still return 500
- **WHEN** an unexpected error occurs (e.g., database connection failure)
- **THEN** the response is HTTP 500 with a generic error message
- **AND** the full exception is logged for debugging
