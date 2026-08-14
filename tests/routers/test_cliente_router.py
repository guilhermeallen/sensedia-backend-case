import pytest
from fastapi.testclient import TestClient

from app.schemas.schemas import ClienteCreate


class TestPostClientes:
    """Test the POST /api/v1/clientes endpoint."""

    def test_criar_cliente_sucesso(self, client):
        """Test successfully creating a client."""
        payload = {
            "nome": "João Silva",
            "email": "joao@example.com",
            "cpf": "12345678900"
        }
        
        response = client.post("/api/v1/clientes", json=payload)
        
        assert response.status_code == 201
        data = response.json()
        assert data["nome"] == "João Silva"
        assert data["email"] == "joao@example.com"
        assert data["cpf"] == "12345678900"
        assert "id" in data

    def test_criar_cliente_nome_com_digito_retorna_400(self, client):
        """Test that creating a client with a name containing digits returns 400."""
        payload = {
            "nome": "João Silva 4",
            "email": "joao@example.com",
            "cpf": "12345678900"
        }
        
        response = client.post("/api/v1/clientes", json=payload)
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "número" in data["detail"].lower()
        assert "não é possível" in data["detail"].lower()

    def test_criar_cliente_nome_multiplos_digitos_retorna_400(self, client):
        """Test that creating a client with a name containing multiple digits returns 400."""
        payload = {
            "nome": "Client 123",
            "email": "client@example.com",
            "cpf": "98765432100"
        }
        
        response = client.post("/api/v1/clientes", json=payload)
        
        assert response.status_code == 400
        assert "detail" in response.json()

    def test_criar_cliente_cpf_duplicado_retorna_400(self, client):
        """Test that creating a client with a duplicate CPF returns 400."""
        payload1 = {
            "nome": "João",
            "email": "joao@example.com",
            "cpf": "12345678900"
        }
        client.post("/api/v1/clientes", json=payload1)
        
        payload2 = {
            "nome": "Maria",
            "email": "maria@example.com",
            "cpf": "12345678900"
        }
        
        response = client.post("/api/v1/clientes", json=payload2)
        
        assert response.status_code == 400
        data = response.json()
        assert "CPF" in data["detail"]

    def test_criar_cliente_email_duplicado_retorna_400(self, client):
        """Test that creating a client with a duplicate email returns 400."""
        payload1 = {
            "nome": "João",
            "email": "joao@example.com",
            "cpf": "12345678900"
        }
        client.post("/api/v1/clientes", json=payload1)
        
        payload2 = {
            "nome": "Maria",
            "email": "joao@example.com",
            "cpf": "98765432100"
        }
        
        response = client.post("/api/v1/clientes", json=payload2)
        
        assert response.status_code == 400
        assert "E-mail" in response.json()["detail"] or "email" in response.json()["detail"].lower()


class TestPutClientes:
    """Test the PUT /api/v1/clientes/{id} endpoint."""

    def test_atualizar_cliente_nome_valido(self, client):
        """Test successfully updating a client's name."""
        # Create client
        payload = {
            "nome": "João",
            "email": "joao@example.com",
            "cpf": "12345678900"
        }
        create_response = client.post("/api/v1/clientes", json=payload)
        cliente_id = create_response.json()["id"]
        
        # Update name
        update_payload = {
            "nome": "João Silva",
            "email": "joao@example.com",
            "cpf": "12345678900"
        }
        response = client.put(f"/api/v1/clientes/{cliente_id}", json=update_payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "João Silva"

    def test_atualizar_cliente_nome_com_digito_retorna_400(self, client):
        """Test that updating a client's name with digits returns 400."""
        # Create client
        payload = {
            "nome": "João",
            "email": "joao@example.com",
            "cpf": "12345678900"
        }
        create_response = client.post("/api/v1/clientes", json=payload)
        cliente_id = create_response.json()["id"]
        
        # Try to update with invalid name
        update_payload = {
            "nome": "João 5",
            "email": "joao@example.com",
            "cpf": "12345678900"
        }
        response = client.put(f"/api/v1/clientes/{cliente_id}", json=update_payload)
        
        assert response.status_code == 400
        data = response.json()
        assert "número" in data["detail"].lower()


class TestPatchClientes:
    """Test the PATCH /api/v1/clientes/{id} endpoint."""

    def test_atualizar_parcial_cliente_nome_valido(self, client):
        """Test successfully partially updating a client's name."""
        # Create client
        payload = {
            "nome": "João",
            "email": "joao@example.com",
            "cpf": "12345678900"
        }
        create_response = client.post("/api/v1/clientes", json=payload)
        cliente_id = create_response.json()["id"]
        
        # Partially update name
        update_payload = {
            "nome": "João Silva"
        }
        response = client.patch(f"/api/v1/clientes/{cliente_id}", json=update_payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "João Silva"
        assert data["email"] == "joao@example.com"  # Unchanged

    def test_atualizar_parcial_cliente_nome_com_digito_retorna_400(self, client):
        """Test that partially updating a client's name with digits returns 400."""
        # Create client
        payload = {
            "nome": "João",
            "email": "joao@example.com",
            "cpf": "12345678900"
        }
        create_response = client.post("/api/v1/clientes", json=payload)
        cliente_id = create_response.json()["id"]
        
        # Try to partially update with invalid name
        update_payload = {
            "nome": "João 99"
        }
        response = client.patch(f"/api/v1/clientes/{cliente_id}", json=update_payload)
        
        assert response.status_code == 400
        data = response.json()
        assert "número" in data["detail"].lower()
