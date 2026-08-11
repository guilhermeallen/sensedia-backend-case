# Spec: Client Name Validation

## ADDED Requirements

### Requirement: Client creation rejects names with digits using HTTP 422
The system SHALL reject any attempt to create a client with a name containing one or more digits (0-9), responding with HTTP 422 (Unprocessable Entity) and a descriptive error message.

#### Scenario: Valid name without digits
- **WHEN** creating a client with name "João Silva"
- **THEN** client is created successfully and returns HTTP 201

#### Scenario: Invalid name with one digit
- **WHEN** creating a client with name "João da Si4lva" (contains digit 4)
- **THEN** the request returns HTTP 422 with detail "Nome inválido: não é permitido incluir números"

#### Scenario: Invalid name with multiple digits
- **WHEN** creating a client with name "Client123"
- **THEN** the request returns HTTP 422 with detail "Nome inválido: não é permitido incluir números"

#### Scenario: Invalid name starts with digit
- **WHEN** creating a client with name "1João"
- **THEN** the request returns HTTP 422 with detail "Nome inválido: não é permitido incluir números"

### Requirement: Client update rejects name changes with digits using HTTP 422
The system SHALL reject any attempt to update a client's name to a value containing one or more digits (0-9), responding with HTTP 422 (Unprocessable Entity) and a descriptive error message.

#### Scenario: Valid name update without digits
- **WHEN** updating an existing client's name to "Maria Santos"
- **THEN** update succeeds and returns HTTP 200

#### Scenario: Invalid name update with digit
- **WHEN** updating an existing client's name to "Maria2Santos" (contains digit 2)
- **THEN** the request returns HTTP 422 with detail "Nome inválido: não é permitido incluir números"

#### Scenario: Update other fields does not trigger name validation
- **WHEN** updating a client's email without changing the name
- **THEN** update succeeds regardless of whether the existing name contains digits

### Requirement: Name validation is consistent across create and update
The system SHALL apply identical name validation rules to both client creation (`POST /clientes`) and client updates (`PUT /clientes/{id}`, `PATCH /clientes/{id}`).

#### Scenario: Same validation rule applies to POST and PUT
- **WHEN** attempting to create a client with name "Test1" and update an existing client to name "Test1"
- **THEN** both requests return HTTP 422 with the same error detail

### Requirement: Other validation rules continue to use HTTP 400
The system SHALL continue to use HTTP 400 (Bad Request) for other validation errors (duplicate CPF, duplicate email), maintaining the existing convention.

#### Scenario: Duplicate CPF returns 400
- **WHEN** creating a client with a CPF already in the database
- **THEN** the request returns HTTP 400 with detail "Já existe um cliente cadastrado com este CPF."

#### Scenario: Duplicate email returns 400
- **WHEN** creating a client with an email already in the database
- **THEN** the request returns HTTP 400 with detail "Já existe um cliente cadastrado com este E-mail."

#### Scenario: Name validation uses 422, not 400
- **WHEN** creating a client with name "Test1"
- **THEN** the request returns HTTP 422, not HTTP 400
