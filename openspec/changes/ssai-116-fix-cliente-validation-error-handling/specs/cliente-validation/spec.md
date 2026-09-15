# Spec: Cliente Validation

## MODIFIED Requirements

### Requirement: Name validation SHALL return HTTP 422 on invalid input
The system SHALL validate that a client name contains no digits (0-9). If a name contains one or more digits, the system SHALL return HTTP 422 Unprocessable Entity with a descriptive JSON error message, not HTTP 500.

#### Scenario: Name contains digits — rejected with 422
- **WHEN** a user attempts to create a client with name "João da Si211217lva" (contains digits)
- **AND** all other fields (CPF, email) are valid and unique
- **THEN** the API returns HTTP 422
- **AND** the response body contains error detail: "Não é possível cadastrar o cliente 'João da Si211217lva': nome contém número, indicando cadastro potencialmente inconsistente."

#### Scenario: Valid name — client created successfully
- **WHEN** a user creates a client with name "João da Silva" (no digits) and valid unique CPF and email
- **THEN** the API returns HTTP 201 Created
- **AND** the client record is stored in the database

#### Scenario: Multiple validation failures — CPF duplicate takes precedence
- **WHEN** a user attempts to create a client with an existing CPF and a name containing digits
- **THEN** the API returns HTTP 400 (CPF duplicate check runs before name validation in current flow)
- **AND** the error message refers to the duplicate CPF, not the invalid name

### Requirement: Name validation error is caught and formatted as JSON
The system SHALL not raise unhandled exceptions when name validation fails. The error SHALL be caught by the FastAPI exception handler and formatted as a proper JSON error response.

#### Scenario: Error response is valid JSON
- **WHEN** a client creation request with invalid name is submitted via POST /clientes
- **THEN** the response Content-Type is application/json
- **AND** the response contains a JSON object with at least "detail" field describing the error

#### Scenario: Middleware can log and track the error
- **WHEN** an invalid name validation triggers an error response
- **THEN** the middleware (if present) can properly log and track the 422 response
- **AND** correlation_id (if used) is preserved in the error handling chain
