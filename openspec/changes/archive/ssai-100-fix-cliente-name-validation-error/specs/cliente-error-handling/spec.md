# Spec: Client Error Handling — Name Validation

## ADDED Requirements

### Requirement: Client Name Validation Must Return HTTP 400

The system SHALL return HTTP 400 (Bad Request) when a client name contains numeric digits, with a clear error message indicating the validation failure.

#### Scenario: Name with digits is rejected with HTTP 400

- **WHEN** a POST request is made to `/api/v1/clientes` with a client name containing one or more digits (e.g., "João da Si211217lva")
- **THEN** the API SHALL return HTTP 400 (Bad Request)
- **AND** the response body SHALL include the detail: "Não é possível cadastrar o cliente '<name>': nome contém número, indicando cadastro potencialmente inconsistente."

#### Scenario: Name without digits is accepted

- **WHEN** a POST request is made to `/api/v1/clientes` with a client name containing no digits (e.g., "João da Silva")
- **AND** all other validation rules pass (CPF and email are unique)
- **THEN** the client SHALL be created successfully with HTTP 201 (Created)

### Requirement: Error Response Format is Consistent with Other Validations

The client name validation error response SHALL follow the same format as other validation errors in the endpoint (e.g., duplicate CPF or email).

#### Scenario: Error response structure matches other validation errors

- **WHEN** a POST request to `/api/v1/clientes` fails any validation (name with digits, duplicate CPF, or duplicate email)
- **THEN** all three errors SHALL return HTTP 400 with a response body containing `{"detail": "error message"}`
- **AND** the structure and semantics SHALL be consistent across all three validations

---

## MODIFIED Requirements

(None — no previously documented client error handling is changed.)

---

## REMOVED Requirements

(None — this change removes no existing requirements.)
