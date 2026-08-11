# Spec: Client Creation Error Handling Consistency

## ADDED Requirements

### Requirement: Validate client name format
The system SHALL reject client creation if the name contains numeric digits.

#### Scenario: Reject name with digit
- **WHEN** POST /clientes is called with `nome` = "João da Si4lva" (contains digit 4)
- **THEN** the system returns HTTP 400 Bad Request
- **AND** the response body contains a detail message explaining the validation failure

#### Scenario: Accept name without digits
- **WHEN** POST /clientes is called with `nome` = "João da Silva" (no digits)
- **THEN** the system proceeds to other validations (CPF, email uniqueness)
- **AND** does not reject based on the digit-in-name rule

### Requirement: Return consistent HTTP status for all client creation validations
The system SHALL return HTTP 400 Bad Request for all validation failures during client creation.

#### Scenario: Name validation failure returns 400
- **WHEN** POST /clientes receives a name with digits
- **THEN** the response status is 400
- **AND** the status matches the CPF duplicate and email duplicate validations

#### Scenario: CPF validation failure returns 400
- **WHEN** POST /clientes receives a CPF that already exists in the database
- **THEN** the response status is 400

#### Scenario: Email validation failure returns 400
- **WHEN** POST /clientes receives an email that already exists in the database
- **THEN** the response status is 400
