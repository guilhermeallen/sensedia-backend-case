"""Repositórios em memória utilizados como fallback quando o banco de dados
está indisponível. Servem exclusivamente para fins de demonstração/teste,
mantendo as rotas de negócio responsivas mesmo com o banco fora do ar."""

from datetime import datetime, timedelta
from itertools import count
from typing import Optional


class _objeto:
    """Wrapper simples que expõe atributos, simulando objetos ORM."""

    def __init__(self, dados: dict):
        self.__dict__.update(dados)

    def __repr__(self):
        return f"_objeto({self.__dict__})"


class MockClienteRepository:
    """Interface mínima exigida pelo ClienteService, sem acesso a banco."""

    def __init__(self):
        self._store = []
        self._seq = count(1)

    def criar(self, cliente):
        novo = {
            "id": next(self._seq),
            "nome": cliente.nome,
            "email": cliente.email,
            "cpf": cliente.cpf,
        }
        self._store.append(novo)
        return _objeto(novo)

    def listar_todos(self):
        return [_objeto(item) for item in self._store]

    def buscar_por_id(self, id: int):
        for item in self._store:
            if item["id"] == id:
                return _objeto(item)
        return None

    def buscar_por_cpf(self, cpf: str):
        for item in self._store:
            if item["cpf"] == cpf:
                return _objeto(item)
        return None

    def buscar_por_email(self, email: str):
        for item in self._store:
            if item["email"] == email:
                return _objeto(item)
        return None

    def deletar(self, cliente):
        self._store[:] = [item for item in self._store if item["id"] != cliente.id]

    def atualizar(self, cliente):
        for idx, item in enumerate(self._store):
            if item["id"] == cliente.id:
                self._store[idx] = {
                    "id": cliente.id,
                    "nome": cliente.nome,
                    "email": cliente.email,
                    "cpf": cliente.cpf,
                }
                return _objeto(self._store[idx])
        return cliente


class MockLogRepository:
    """Interface mínima exigida pelo LogService, sem acesso a banco."""

    def __init__(self):
        self._store = [
            {
                "id": 1,
                "timestamp": datetime.now() - timedelta(minutes=5),
                "level": "INFO",
                "message": "[mock] Log de exemplo 1 - requisição processada.",
                "correlation_id": "mock-correlacao-0001",
                "endpoint": "/api/v1/clientes",
                "method": "POST",
                "status_code": 409,
                "traceback": None,
                "module": "app.main",
            },
            {
                "id": 2,
                "timestamp": datetime.now() - timedelta(hours=1),
                "level": "ERROR",
                "message": (
                    "[mock] Erro simulado: nome contém número, indicando cadastro "
                    "potencialmente inconsistente."
                ),
                "correlation_id": "mock-correlacao-0002",
                "endpoint": "/api/v1/clientes",
                "method": "POST",
                "status_code": 422,
                "traceback": "RuntimeError: ...",
                "module": "app.services.cliente_service",
            },
            {
                "id": 3,
                "timestamp": datetime.now() - timedelta(days=1),
                "level": "WARNING",
                "message": "[mock] Warning de exemplo - tempo de resposta elevado.",
                "correlation_id": "mock-correlacao-0003",
                "endpoint": "/api/v1/apolices",
                "method": "GET",
                "status_code": 504,
                "traceback": None,
                "module": "app.main",
            },
        ]
        self._seq = count(len(self._store) + 1)

    def buscar_com_filtros(
        self,
        data_inicio: Optional[datetime] = None,
        data_fim: Optional[datetime] = None,
        level: Optional[str] = None,
        status_code: Optional[int] = None,
        limit: int = 5,
        offset: int = 0,
    ) -> list:
        items = sorted(self._store, key=lambda i: i["timestamp"], reverse=True)

        if data_inicio is not None:
            items = [i for i in items if i["timestamp"] >= data_inicio]
        if data_fim is not None:
            items = [i for i in items if i["timestamp"] <= data_fim]
        if level is not None:
            items = [i for i in items if i["level"].upper() == level.upper()]
        if status_code is not None:
            items = [i for i in items if i["status_code"] == status_code]

        return [_objeto(i) for i in items[offset:offset + limit]]

    def criar(self, log):
        registro = {
            "id": next(self._seq),
            "timestamp": log.timestamp or datetime.now(),
            "level": log.level,
            "message": log.message,
            "correlation_id": log.correlation_id,
            "endpoint": log.endpoint,
            "method": log.method,
            "status_code": log.status_code,
            "traceback": log.traceback,
            "module": log.module,
        }
        self._store.append(registro)
        return _objeto(registro)

    def remover_todos(self) -> int:
        qtd = len(self._store)
        self._store.clear()
        return qtd
