import pytest
from unittest.mock import Mock
from fastapi import HTTPException, status
from app.services.cliente_service import ClienteService
from app.schemas.schemas import ClienteCreate


class TestClienteServiceNameValidation:
    """Test client name validation error handling."""

    @pytest.fixture
    def mock_db(self):
        """Create a mock database session."""
        return Mock()

    @pytest.fixture
    def service(self, mock_db):
        """Create a ClienteService with a mock repository."""
        return ClienteService(mock_db)

    @pytest.fixture
    def valid_client_data(self):
        """Create valid client data without digits in name."""
        return ClienteCreate(
            nome="João da Silva",
            email="joao@example.com",
            cpf="12345678901234"
        )

    @pytest.fixture
    def client_with_digit_name(self):
        """Create client data with digits in name."""
        return ClienteCreate(
            nome="João da Si211217lva",
            email="joao@example.com",
            cpf="12345678901234"
        )

    def test_name_with_digits_raises_http_400(self, service, client_with_digit_name):
        """
        Test that a client name containing digits raises HTTPException with status 400.
        This is a regression test for SSAI-100: should be 400, not 500.
        """
        with pytest.raises(HTTPException) as exc_info:
            service.criar_cliente(client_with_digit_name)

        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "nome contém número" in exc_info.value.detail
        assert "João da Si211217lva" in exc_info.value.detail

    def test_name_with_digits_error_message(self, service, client_with_digit_name):
        """Test that the error message is clear and descriptive."""
        with pytest.raises(HTTPException) as exc_info:
            service.criar_cliente(client_with_digit_name)

        expected_detail = (
            f"Não é possível cadastrar o cliente '{client_with_digit_name.nome}': "
            f"nome contém número, indicando cadastro potencialmente inconsistente."
        )
        assert exc_info.value.detail == expected_detail

    def test_name_without_digits_passes_validation(self, service, valid_client_data):
        """
        Test that a client name without digits passes the name validation
        and continues to other validations (this tests the happy path flow).
        """
        # Mock the repository to return None for lookups (no duplicates)
        service.repository.buscar_por_cpf = Mock(return_value=None)
        service.repository.buscar_por_email = Mock(return_value=None)
        mock_client = Mock()
        service.repository.criar = Mock(return_value=mock_client)

        result = service.criar_cliente(valid_client_data)

        # Verify the client was created (no exception raised)
        assert result == mock_client
        service.repository.criar.assert_called_once_with(valid_client_data)

    def test_cpf_validation_still_returns_400(self, service, valid_client_data):
        """
        Test that CPF duplicate validation also returns 400.
        This ensures consistency across all validation errors.
        """
        service.repository.buscar_por_cpf = Mock(return_value=Mock())

        with pytest.raises(HTTPException) as exc_info:
            service.criar_cliente(valid_client_data)

        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "CPF" in exc_info.value.detail

    def test_email_validation_still_returns_400(self, service, valid_client_data):
        """
        Test that email duplicate validation also returns 400.
        This ensures consistency across all validation errors.
        """
        service.repository.buscar_por_cpf = Mock(return_value=None)
        service.repository.buscar_por_email = Mock(return_value=Mock())

        with pytest.raises(HTTPException) as exc_info:
            service.criar_cliente(valid_client_data)

        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "E-mail" in exc_info.value.detail

    @pytest.mark.parametrize("name", [
        "João 2º Silva",
        "María José 3",
        "José da Silva123",
        "A1B2C3",
        "João0"
    ])
    def test_various_names_with_digits_rejected(self, service, name):
        """
        Test that various patterns of digits in names are all rejected with 400.
        """
        client_data = ClienteCreate(
            nome=name,
            email="test@example.com",
            cpf="12345678901234"
        )

        with pytest.raises(HTTPException) as exc_info:
            service.criar_cliente(client_data)

        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "nome contém número" in exc_info.value.detail
