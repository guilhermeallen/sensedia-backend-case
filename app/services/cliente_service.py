from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.cliente_repo import ClienteRepository
from app.schemas.schemas import ClienteCreate

class ClienteService:
    def __init__(self, db: Session):
        self.repository = ClienteRepository(db)

    def criar_cliente(self, dados_cliente: ClienteCreate):
        # Regra de Negócio 1: Verificar CPF duplicado
        if self.repository.buscar_por_cpf(dados_cliente.cpf):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe um cliente cadastrado com este CPF."
            )
        
        # Regra de Negócio 2: Verificar Email duplicado
        if self.repository.buscar_por_email(dados_cliente.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe um cliente cadastrado com este E-mail."
            )
            
        return self.repository.criar(dados_cliente)

    def listar_clientes(self):
        return self.repository.listar_todos()

    def buscar_cliente(self, id: int):
        cliente = self.repository.buscar_por_id(id)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente não encontrado."
            )
        return cliente