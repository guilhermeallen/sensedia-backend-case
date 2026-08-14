# Especificação — Tratamento de Erros de Validação no Registro de Clientes

## ADDED Requirements

### Requirement: Cliente POST endpoint SHALL return HTTP 400 for all validation failures
The system SHALL catch all validation errors during cliente creation (name, CPF, email) and return HTTP 400 Bad Request with a descriptive error message, rather than allowing unhandled exceptions to bubble up as HTTP 500.

#### Scenario: Name contains numeric digits
- **WHEN** POST /clientes receives a request with `nome` containing one or more digits (e.g., "João Silva4" or "123")
- **THEN** the endpoint returns HTTP 400 Bad Request with `detail` describing the validation failure
- **AND** no HTTP 500 error is logged

#### Scenario: CPF already registered
- **WHEN** POST /clientes receives a request with a CPF already in the database (exact duplicate)
- **THEN** the endpoint returns HTTP 400 Bad Request with detail "Já existe um cliente cadastrado com este CPF."
- **AND** the response status is consistent with name validation failure (both 400)

#### Scenario: Email already registered
- **WHEN** POST /clientes receives a request with an email already in the database (exact duplicate)
- **THEN** the endpoint returns HTTP 400 Bad Request with detail "Já existe um cliente cadastrado com este E-mail."
- **AND** the response status is consistent with name validation failure (both 400)

#### Scenario: Valid request succeeds
- **WHEN** POST /clientes receives a request with valid `nome` (no digits), unique CPF, and unique email
- **THEN** the endpoint returns HTTP 201 Created with the new client data
- **AND** the client is stored in the database

### Requirement: Error message SHALL be descriptive
The system SHALL provide a clear error message in the HTTP response body (`detail` field) that explains what validation rule was violated, enabling clients to correct the input.

#### Scenario: Name validation error message
- **WHEN** POST /clientes receives `nome` with digits
- **THEN** the response includes a message indicating that the name contains numbers and cannot be registered
- **AND** the message is in Portuguese (matching the existing system language)

#### Scenario: Duplicate CPF error message
- **WHEN** POST /clientes receives a CPF that already exists
- **THEN** the response includes "Já existe um cliente cadastrado com este CPF." (existing message unchanged)

#### Scenario: Duplicate email error message
- **WHEN** POST /clientes receives an email that already exists
- **THEN** the response includes "Já existe um cliente cadastrado com este E-mail." (existing message unchanged)
