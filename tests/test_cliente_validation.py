import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestClienteNameValidation:
    """Tests for client name validation in create and update operations."""

    def test_create_cliente_with_valid_name(self, db):
        """POST /clientes with valid name (no digits) should return 201."""
        response = client.post(
            "/api/v1/clientes",
            json={
                "nome": "João Silva",
                "email": "joao@example.com",
                "cpf": "12345678901"
            }
        )
        assert response.status_code == 201
        assert response.json()["nome"] == "João Silva"

    def test_create_cliente_with_name_containing_one_digit(self, db):
        """POST /clientes with name containing digit should return 422."""
        response = client.post(
            "/api/v1/clientes",
            json={
                "nome": "João da Si4lva",
                "email": "joao@example.com",
                "cpf": "12345678901"
            }
        )
        assert response.status_code == 422
        assert "Nome inválido" in response.json()["detail"]
        assert "números" in response.json()["detail"]

    def test_create_cliente_with_name_containing_multiple_digits(self, db):
        """POST /clientes with name containing multiple digits should return 422."""
        response = client.post(
            "/api/v1/clientes",
            json={
                "nome": "Client123",
                "email": "client@example.com",
                "cpf": "12345678902"
            }
        )
        assert response.status_code == 422
        assert "Nome inválido" in response.json()["detail"]

    def test_create_cliente_with_name_starting_with_digit(self, db):
        """POST /clientes with name starting with digit should return 422."""
        response = client.post(
            "/api/v1/clientes",
            json={
                "nome": "1João",
                "email": "joao2@example.com",
                "cpf": "12345678903"
            }
        )
        assert response.status_code == 422
        assert "Nome inválido" in response.json()["detail"]

    def test_update_cliente_with_valid_name(self, db):
        """PUT /clientes/{id} with valid name should return 200."""
        # First create a client
        create_response = client.post(
            "/api/v1/clientes",
            json={
                "nome": "Original Name",
                "email": "original@example.com",
                "cpf": "10000000001"
            }
        )
        assert create_response.status_code == 201
        cliente_id = create_response.json()["id"]

        # Update with valid name
        update_response = client.put(
            f"/api/v1/clientes/{cliente_id}",
            json={
                "nome": "Maria Santos",
                "email": "original@example.com",
                "cpf": "10000000001"
            }
        )
        assert update_response.status_code == 200
        assert update_response.json()["nome"] == "Maria Santos"

    def test_update_cliente_with_invalid_name(self, db):
        """PUT /clientes/{id} with invalid name should return 422."""
        # First create a client
        create_response = client.post(
            "/api/v1/clientes",
            json={
                "nome": "Original Name",
                "email": "original@example.com",
                "cpf": "10000000002"
            }
        )
        assert create_response.status_code == 201
        cliente_id = create_response.json()["id"]

        # Update with invalid name
        update_response = client.put(
            f"/api/v1/clientes/{cliente_id}",
            json={
                "nome": "Maria2Santos",
                "email": "original@example.com",
                "cpf": "10000000002"
            }
        )
        assert update_response.status_code == 422
        assert "Nome inválido" in update_response.json()["detail"]

    def test_patch_cliente_with_valid_name(self, db):
        """PATCH /clientes/{id} with valid name should return 200."""
        # First create a client
        create_response = client.post(
            "/api/v1/clientes",
            json={
                "nome": "Original Name",
                "email": "original@example.com",
                "cpf": "10000000003"
            }
        )
        assert create_response.status_code == 201
        cliente_id = create_response.json()["id"]

        # Update with valid name via PATCH
        update_response = client.patch(
            f"/api/v1/clientes/{cliente_id}",
            json={"nome": "New Valid Name"}
        )
        assert update_response.status_code == 200
        assert update_response.json()["nome"] == "New Valid Name"

    def test_patch_cliente_with_invalid_name(self, db):
        """PATCH /clientes/{id} with invalid name should return 422."""
        # First create a client
        create_response = client.post(
            "/api/v1/clientes",
            json={
                "nome": "Original Name",
                "email": "original@example.com",
                "cpf": "10000000004"
            }
        )
        assert create_response.status_code == 201
        cliente_id = create_response.json()["id"]

        # Update with invalid name via PATCH
        update_response = client.patch(
            f"/api/v1/clientes/{cliente_id}",
            json={"nome": "Invalid3Name"}
        )
        assert update_response.status_code == 422
        assert "Nome inválido" in update_response.json()["detail"]

    def test_patch_cliente_without_name_field_skips_validation(self, db):
        """PATCH /clientes/{id} without name field should skip name validation."""
        # First create a client
        create_response = client.post(
            "/api/v1/clientes",
            json={
                "nome": "Original Name",
                "email": "original@example.com",
                "cpf": "10000000005"
            }
        )
        assert create_response.status_code == 201
        cliente_id = create_response.json()["id"]

        # Update other field without touching name
        update_response = client.patch(
            f"/api/v1/clientes/{cliente_id}",
            json={"email": "newemail@example.com"}
        )
        assert update_response.status_code == 200
        assert update_response.json()["email"] == "newemail@example.com"

    def test_duplicate_cpf_returns_400_not_422(self, db):
        """POST /clientes with duplicate CPF should return 400, not 422."""
        # Create first client
        client1_response = client.post(
            "/api/v1/clientes",
            json={
                "nome": "First Client",
                "email": "first@example.com",
                "cpf": "99999999999"
            }
        )
        assert client1_response.status_code == 201

        # Try to create another with same CPF
        client2_response = client.post(
            "/api/v1/clientes",
            json={
                "nome": "Second Client",
                "email": "second@example.com",
                "cpf": "99999999999"
            }
        )
        assert client2_response.status_code == 400
        assert "CPF" in client2_response.json()["detail"]

    def test_duplicate_email_returns_400_not_422(self, db):
        """POST /clientes with duplicate email should return 400, not 422."""
        # Create first client
        client1_response = client.post(
            "/api/v1/clientes",
            json={
                "nome": "First Client",
                "email": "duplicate@example.com",
                "cpf": "88888888888"
            }
        )
        assert client1_response.status_code == 201

        # Try to create another with same email
        client2_response = client.post(
            "/api/v1/clientes",
            json={
                "nome": "Second Client",
                "email": "duplicate@example.com",
                "cpf": "77777777777"
            }
        )
        assert client2_response.status_code == 400
        assert "E-mail" in client2_response.json()["detail"]
