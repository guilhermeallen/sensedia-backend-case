# Spec: Cliente Validation Error Handling

## ADDED Requirements

### Requirement: Invalid name validation returns HTTP 400
The system SHALL return HTTP 400 Bad Request when a customer's name contains digits during creation, not HTTP 500 Internal Server Error.

#### Scenario: Name with digits is rejected with 400
- **WHEN** a POST request to `/clientes` includes a name containing digits (e.g., "João Silva 123")
- **THEN** the endpoint responds with HTTP 400 Bad Request
- **AND** the response body includes a detail message explaining the validation failure

#### Scenario: Valid name without digits is accepted
- **WHEN** a POST request to `/clientes` includes a valid name without digits (e.g., "João Silva")
- **AND** the CPF and email are not duplicated
- **THEN** the endpoint responds with HTTP 201 Created
- **AND** the customer is created successfully

#### Scenario: Error message is consistent with other validation errors
- **WHEN** a POST request to `/clientes` fails validation (name with digits)
- **AND** other validation rules (duplicate CPF, duplicate email) also fail
- **THEN** all validation error responses follow the same structure and status code (HTTP 400)

### Requirement: Exception handling aligns with code convention
The system SHALL raise `HTTPException` with an appropriate 4xx status for all validation failures in customer creation, matching the pattern used for duplicate CPF and email validation.

#### Scenario: Name validation uses HTTPException like sibling rules
- **WHEN** the `ClienteService.criar_cliente()` method detects an invalid name
- **THEN** it raises `HTTPException(status_code=400, detail=...)` 
- **AND** NOT a bare `RuntimeError`
- **AND** the global exception handler treats it the same as duplicate CPF/email errors

#### Scenario: Validation failure is not treated as an internal server error
- **WHEN** the validation rule for names is triggered
- **THEN** the FastAPI global exception handler routes it to `http_exception_handler`, not `generic_exception_handler`
- **AND** it does not produce a 500 response

## MODIFIED Requirements
(None — the behavior of name validation itself remains unchanged; only the error type is corrected)

## REMOVED Requirements
(None)

## RENAMED Requirements
(None)
