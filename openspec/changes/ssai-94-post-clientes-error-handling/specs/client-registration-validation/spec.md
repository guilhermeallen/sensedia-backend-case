# Spec — client-registration-validation

## MODIFIED Requirements

### Requirement: Name validation SHALL return HTTP 400 for invalid inputs
The `POST /clientes` endpoint SHALL reject client names that contain numeric digits and return an HTTP 400 Bad Request response with a clear error message, consistent with other validation rules on the same endpoint.

#### Scenario: Name with digits is rejected with 400
- **WHEN** a POST request to `/clientes` includes a client name containing one or more digits (e.g., "João da Si4lva")
- **THEN** the endpoint returns HTTP 400 Bad Request
- **AND** the response body includes a detail message indicating the name contains invalid characters

#### Scenario: Valid name is accepted
- **WHEN** a POST request to `/clientes` includes a valid client name without digits (e.g., "João da Silva")
- **AND** the CPF and email are unique
- **THEN** the endpoint returns HTTP 201 Created
- **AND** the client record is created in the database

### Requirement: All validation failures SHALL return 4xx errors
The `ClienteService.criar_cliente()` method SHALL ensure all validation rules raise `HTTPException` with appropriate 4xx status codes, not bare exceptions that would result in 500 errors.

#### Scenario: Duplicate CPF returns 400
- **WHEN** a POST request to `/clientes` includes a CPF already registered to another client
- **THEN** the endpoint returns HTTP 400 Bad Request
- **AND** the response includes a message about the duplicate CPF

#### Scenario: Duplicate email returns 400
- **WHEN** a POST request to `/clientes` includes an email already registered to another client
- **THEN** the endpoint returns HTTP 400 Bad Request
- **AND** the response includes a message about the duplicate email

#### Scenario: All three validations fail consistently
- **WHEN** the POST `/clientes` endpoint validates client names, CPFs, or emails
- **THEN** invalid inputs trigger validation errors
- **AND** all validation errors return HTTP 400 (not 500)
- **AND** error messages are consistent in format and clarity
