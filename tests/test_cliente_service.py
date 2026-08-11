"""
Unit tests for ClienteService name validation logic.
These tests verify the HTTP 422 error is raised for invalid names.
"""
import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException, status
from app.services.cliente_service import ClienteService
from app.schemas.schemas import ClienteCreate


@pytest.fixture
def mock_db():
    """Mock SQLAlchemy session."""
    return Mock()


@pytest.fixture
def service(mock_db):
    """Create a ClienteService with mocked repository."""
    return ClienteService(db=mock_db)


class TestClienteServiceNameValidation:
    """Test name validation in ClienteService."""

    def test_validar_nome_with_valid_name(self, service):
        """_validar_nome should not raise for names without digits."""
        # Should not raise
        service._validar_nome("João Silva")
        service._validar_nome("Maria Santos")
        service._validar_nome("José dos Santos")

    def test_validar_nome_with_name_containing_digit(self, service):
        """_validar_nome should raise HTTP 422 for names containing digits."""
        with pytest.raises(HTTPException) as exc_info:
            service._validar_nome("João da Si4lva")
        
        assert exc_info.value.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "Nome inválido" in exc_info.value.detail
        assert "números" in exc_info.value.detail

    def test_validar_nome_with_digit_at_start(self, service):
        """_validar_nome should raise HTTP 422 for names starting with digit."""
        with pytest.raises(HTTPException) as exc_info:
            service._validar_nome("1João")
        
        assert exc_info.value.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_validar_nome_with_multiple_digits(self, service):
        """_validar_nome should raise HTTP 422 for names with multiple digits."""
        with pytest.raises(HTTPException) as exc_info:
            service._validar_nome("Client123")
        
        assert exc_info.value.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_criar_cliente_validates_name(self, service, mock_db):
        """criar_cliente should validate name before checking duplicates."""
        mock_db.buscar_por_cpf = Mock(return_value=None)
        mock_db.buscar_por_email = Mock(return_value=None)

        # Mock repository to avoid actual DB calls
        with patch.object(service.repository, 'buscar_por_cpf', return_value=None):
            with patch.object(service.repository, 'buscar_por_email', return_value=None):
                # Invalid name should raise 422
                with pytest.raises(HTTPException) as exc_info:
                    service.criar_cliente(ClienteCreate(
                        nome="João2Silva",
                        email="joao@example.com",
                        cpf="12345678901"
                    ))
                assert exc_info.value.status_code == 422

    def test_atualizar_cliente_validates_name_when_changed(self, service, mock_db):
        """atualizar_cliente should validate name if being updated."""
        mock_cliente = Mock()
        mock_cliente.id = 1
        mock_cliente.cpf = "12345678901"
        mock_cliente.email = "old@example.com"

        with patch.object(service, 'buscar_cliente', return_value=mock_cliente):
            # Invalid name should raise 422
            with pytest.raises(HTTPException) as exc_info:
                service.atualizar_cliente(1, {"nome": "João5Silva"})
            assert exc_info.value.status_code == 422

    def test_atualizar_cliente_skips_name_validation_if_not_changed(self, service, mock_db):
        """atualizar_cliente should not validate name if not in update dict."""
        mock_cliente = Mock()
        mock_cliente.id = 1
        mock_cliente.cpf = "12345678901"
        mock_cliente.email = "old@example.com"

        with patch.object(service, 'buscar_cliente', return_value=mock_cliente):
            with patch.object(service.repository, 'buscar_por_email', return_value=None):
                with patch.object(service.repository, 'atualizar', return_value=mock_cliente):
                    # Update without nome should not raise name validation error
                    result = service.atualizar_cliente(1, {"email": "new@example.com"})
                    assert result is not None

    def test_criar_cliente_validates_cpf_duplicate(self, service, mock_db):
        """criar_cliente should return 400 for duplicate CPF (not 422)."""
        mock_cliente_existing = Mock()

        with patch.object(service.repository, 'buscar_por_cpf', return_value=mock_cliente_existing):
            with pytest.raises(HTTPException) as exc_info:
                service.criar_cliente(ClienteCreate(
                    nome="João Silva",
                    email="joao@example.com",
                    cpf="12345678901"
                ))
            assert exc_info.value.status_code == 400
            assert "CPF" in exc_info.value.detail

    def test_criar_cliente_validates_email_duplicate(self, service, mock_db):
        """criar_cliente should return 400 for duplicate email (not 422)."""
        mock_cliente_existing = Mock()

        with patch.object(service.repository, 'buscar_por_cpf', return_value=None):
            with patch.object(service.repository, 'buscar_por_email', return_value=mock_cliente_existing):
                with pytest.raises(HTTPException) as exc_info:
                    service.criar_cliente(ClienteCreate(
                        nome="João Silva",
                        email="duplicate@example.com",
                        cpf="12345678901"
                    ))
                assert exc_info.value.status_code == 400
                assert "E-mail" in exc_info.value.detail
