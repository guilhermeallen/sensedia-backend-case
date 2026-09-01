# Specification: Client Validation Error Response

## MODIFIED Requirements

### Requirement: Client name must not contain digits
The system SHALL reject client names that contain digits and return HTTP 400 (Bad Request) with a clear error message.

#### Scenario: Create client with digit in name
- **GIVEN** a `POST /clientes` request with a valid client email and CPF
- **WHEN** the client name contains one or more digits (e.g., "João3 Silva", "Jo0e3on da Si211217lva")
- **THEN** the API returns HTTP 400 (Bad Request)
- **AND** the response body contains a detail field explaining the rejection: "Não é possível cadastrar o cliente: nome contém número"
- **AND** the error is logged at WARNING level with correlation_id, endpoint, method, status_code (400), and module

#### Scenario: Create client with valid name (no digits)
- **GIVEN** a `POST /clientes` request with a valid client name (no digits), email, and CPF
- **WHEN** no other validation rules are violated (CPF and email uniqueness)
- **THEN** the API returns HTTP 201 (Created)
- **AND** the client is successfully registered in the database

### Requirement: Client email must be unique
The system SHALL reject duplicate emails and return HTTP 400 (Bad Request).

#### Scenario: Create client with duplicate email
- **GIVEN** a client with email "joao@example.com" already exists in the database
- **WHEN** a `POST /clientes` request is submitted with the same email
- **THEN** the API returns HTTP 400 (Bad Request)
- **AND** the detail field states: "Já existe um cliente cadastrado com este E-mail."

### Requirement: Client CPF must be unique
The system SHALL reject duplicate CPFs and return HTTP 400 (Bad Request).

#### Scenario: Create client with duplicate CPF
- **GIVEN** a client with CPF "12345678901" already exists in the database
- **WHEN** a `POST /clientes` request is submitted with the same CPF
- **THEN** the API returns HTTP 400 (Bad Request)
- **AND** the detail field states: "Já existe um cliente cadastrado com este CPF."
