"""Tests for ClienteService validation and error handling."""

import pytest
from unittest.mock import Mock, MagicMock
from fastapi import HTTPException, status

from app.services.cliente_service import ClienteService
from app.schemas.schemas import ClienteCreate


class TestClienteServiceValidation:
    """Test suite for ClienteService validation logic."""

    def test_criar_cliente_with_digits_in_name_returns_422(self):
        """Test that name containing digits raises HTTPException with 422 status."""
        # Arrange
        mock_db = Mock()
        service = ClienteService(db=mock_db)
        
        dados = ClienteCreate(
            nome="João da Si211217lva",
            cpf="12345678901",
            email="joao@example.com"
        )
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.criar_cliente(dados)
        
        assert exc_info.value.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "João da Si211217lva" in exc_info.value.detail
        assert "contém número" in exc_info.value.detail

    def test_criar_cliente_valid_name_without_digits(self):
        """Test that valid name without digits proceeds to duplicate checks."""
        # Arrange
        mock_repo = Mock()
        mock_repo.buscar_por_cpf.return_value = None
        mock_repo.buscar_por_email.return_value = None
        mock_repo.criar.return_value = {"id": 1, "nome": "João da Silva"}
        
        mock_db = Mock()
        service = ClienteService(db=mock_db)
        service.repository = mock_repo
        
        dados = ClienteCreate(
            nome="João da Silva",
            cpf="12345678901",
            email="joao@example.com"
        )
        
        # Act
        result = service.criar_cliente(dados)
        
        # Assert
        assert result is not None
        mock_repo.criar.assert_called_once_with(dados)

    def test_criar_cliente_cpf_duplicate_returns_400(self):
        """Test that duplicate CPF check still returns 400 (not affected by fix)."""
        # Arrange
        mock_repo = Mock()
        mock_repo.buscar_por_cpf.return_value = {"id": 1}  # CPF already exists
        
        mock_db = Mock()
        service = ClienteService(db=mock_db)
        service.repository = mock_repo
        
        dados = ClienteCreate(
            nome="João da Silva",
            cpf="12345678901",
            email="joao@example.com"
        )
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.criar_cliente(dados)
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "CPF" in exc_info.value.detail

    def test_criar_cliente_email_duplicate_returns_400(self):
        """Test that duplicate email check still returns 400 (not affected by fix)."""
        # Arrange
        mock_repo = Mock()
        mock_repo.buscar_por_cpf.return_value = None
        mock_repo.buscar_por_email.return_value = {"id": 1}  # Email already exists
        
        mock_db = Mock()
        service = ClienteService(db=mock_db)
        service.repository = mock_repo
        
        dados = ClienteCreate(
            nome="João da Silva",
            cpf="12345678901",
            email="joao@example.com"
        )
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.criar_cliente(dados)
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "E-mail" in exc_info.value.detail

    @pytest.mark.parametrize("invalid_name", [
        "João1Silva",
        "Maria2",
        "123",
        "Test9Name",
        "A0",
    ])
    def test_criar_cliente_various_digits_in_names(self, invalid_name):
        """Test that various names with digits all raise 422."""
        # Arrange
        mock_db = Mock()
        service = ClienteService(db=mock_db)
        
        dados = ClienteCreate(
            nome=invalid_name,
            cpf="12345678901",
            email="test@example.com"
        )
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.criar_cliente(dados)
        
        assert exc_info.value.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_exception_has_descriptive_message(self):
        """Test that the exception message is descriptive and contains client info."""
        # Arrange
        mock_db = Mock()
        service = ClienteService(db=mock_db)
        
        invalid_name = "Test1Name"
        dados = ClienteCreate(
            nome=invalid_name,
            cpf="12345678901",
            email="test@example.com"
        )
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.criar_cliente(dados)
        
        exception = exc_info.value
        assert invalid_name in exception.detail
        assert "inconsistente" in exception.detail.lower()
