import pytest
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.services.cliente_service import ClienteService
from app.schemas.schemas import ClienteCreate
from app.models.models import Cliente


@pytest.fixture
def service(test_db):
    """Create a ClienteService instance with a test database."""
    return ClienteService(test_db)


class TestNomeValidacao:
    """Test the _validar_nome method."""

    def test_validar_nome_valido(self, service):
        """Test that a valid name (without digits) passes validation."""
        # Should not raise
        service._validar_nome("João Silva")
        service._validar_nome("Maria da Silva")
        service._validar_nome("José")

    def test_validar_nome_com_um_digito(self, service):
        """Test that a name with a single digit fails validation."""
        with pytest.raises(HTTPException) as exc_info:
            service._validar_nome("João 5")
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "número" in exc_info.value.detail.lower()
        assert "João 5" in exc_info.value.detail

    def test_validar_nome_com_multiplos_digitos(self, service):
        """Test that a name with multiple digits fails validation."""
        with pytest.raises(HTTPException) as exc_info:
            service._validar_nome("Cliente 123")
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "número" in exc_info.value.detail.lower()

    def test_validar_nome_apenas_digitos(self, service):
        """Test that a name that is only digits fails validation."""
        with pytest.raises(HTTPException) as exc_info:
            service._validar_nome("12345")
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST

    def test_validar_nome_com_digito_no_meio(self, service):
        """Test that a name with a digit anywhere in it fails."""
        with pytest.raises(HTTPException) as exc_info:
            service._validar_nome("João Silva 3rd")
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST


class TestCriarCliente:
    """Test the criar_cliente method."""

    def test_criar_cliente_valido(self, service, test_db):
        """Test creating a valid client."""
        cliente_data = ClienteCreate(
            nome="João Silva",
            email="joao@example.com",
            cpf="12345678900"
        )
        
        cliente = service.criar_cliente(cliente_data)
        
        assert cliente.id is not None
        assert cliente.nome == "João Silva"
        assert cliente.email == "joao@example.com"
        assert cliente.cpf == "12345678900"

    def test_criar_cliente_nome_com_digito_falha(self, service):
        """Test that creating a client with a name containing digits fails."""
        cliente_data = ClienteCreate(
            nome="João Silva 4",
            email="joao@example.com",
            cpf="12345678900"
        )
        
        with pytest.raises(HTTPException) as exc_info:
            service.criar_cliente(cliente_data)
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "número" in exc_info.value.detail.lower()

    def test_criar_cliente_cpf_duplicado_falha(self, service, test_db):
        """Test that creating a client with a duplicate CPF fails."""
        # Create first client
        cliente1 = ClienteCreate(
            nome="João",
            email="joao1@example.com",
            cpf="12345678900"
        )
        service.criar_cliente(cliente1)
        
        # Try to create second client with same CPF
        cliente2 = ClienteCreate(
            nome="Maria",
            email="maria@example.com",
            cpf="12345678900"
        )
        
        with pytest.raises(HTTPException) as exc_info:
            service.criar_cliente(cliente2)
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "CPF" in exc_info.value.detail

    def test_criar_cliente_email_duplicado_falha(self, service):
        """Test that creating a client with a duplicate email fails."""
        # Create first client
        cliente1 = ClienteCreate(
            nome="João",
            email="joao@example.com",
            cpf="12345678900"
        )
        service.criar_cliente(cliente1)
        
        # Try to create second client with same email
        cliente2 = ClienteCreate(
            nome="Maria",
            email="joao@example.com",
            cpf="98765432100"
        )
        
        with pytest.raises(HTTPException) as exc_info:
            service.criar_cliente(cliente2)
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "E-mail" in exc_info.value.detail or "email" in exc_info.value.detail.lower()


class TestAtualizarCliente:
    """Test the atualizar_cliente method."""

    def test_atualizar_nome_valido(self, service):
        """Test updating a client with a valid name."""
        # Create client
        cliente_data = ClienteCreate(
            nome="João",
            email="joao@example.com",
            cpf="12345678900"
        )
        cliente = service.criar_cliente(cliente_data)
        
        # Update with valid name
        atualizado = service.atualizar_cliente(cliente.id, {"nome": "João Silva"})
        
        assert atualizado.nome == "João Silva"

    def test_atualizar_nome_com_digito_falha(self, service):
        """Test that updating a client with a name containing digits fails."""
        # Create client
        cliente_data = ClienteCreate(
            nome="João",
            email="joao@example.com",
            cpf="12345678900"
        )
        cliente = service.criar_cliente(cliente_data)
        
        # Try to update with invalid name
        with pytest.raises(HTTPException) as exc_info:
            service.atualizar_cliente(cliente.id, {"nome": "João 5"})
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "número" in exc_info.value.detail.lower()

    def test_atualizar_cpf_duplicado_falha(self, service):
        """Test that updating a client with a duplicate CPF fails."""
        # Create two clients
        cliente1_data = ClienteCreate(
            nome="João",
            email="joao@example.com",
            cpf="12345678900"
        )
        cliente1 = service.criar_cliente(cliente1_data)
        
        cliente2_data = ClienteCreate(
            nome="Maria",
            email="maria@example.com",
            cpf="98765432100"
        )
        cliente2 = service.criar_cliente(cliente2_data)
        
        # Try to update cliente2's CPF to cliente1's CPF
        with pytest.raises(HTTPException) as exc_info:
            service.atualizar_cliente(cliente2.id, {"cpf": "12345678900"})
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "CPF" in exc_info.value.detail

    def test_atualizar_email_duplicado_falha(self, service):
        """Test that updating a client with a duplicate email fails."""
        # Create two clients
        cliente1_data = ClienteCreate(
            nome="João",
            email="joao@example.com",
            cpf="12345678900"
        )
        cliente1 = service.criar_cliente(cliente1_data)
        
        cliente2_data = ClienteCreate(
            nome="Maria",
            email="maria@example.com",
            cpf="98765432100"
        )
        cliente2 = service.criar_cliente(cliente2_data)
        
        # Try to update cliente2's email to cliente1's email
        with pytest.raises(HTTPException) as exc_info:
            service.atualizar_cliente(cliente2.id, {"email": "joao@example.com"})
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST

    def test_atualizar_multiplos_campos(self, service):
        """Test updating multiple fields of a client."""
        # Create client
        cliente_data = ClienteCreate(
            nome="João",
            email="joao@example.com",
            cpf="12345678900"
        )
        cliente = service.criar_cliente(cliente_data)
        
        # Update multiple fields
        atualizado = service.atualizar_cliente(cliente.id, {
            "nome": "João Silva",
            "email": "joao.silva@example.com"
        })
        
        assert atualizado.nome == "João Silva"
        assert atualizado.email == "joao.silva@example.com"
