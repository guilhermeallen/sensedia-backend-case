# Proposta de Mudança — SSAI-114

## Por Que?

O endpoint POST /clientes está retornando HTTP 500 em resposta a requisições válidas em QA. A análise agentica identificou que o serviço de cadastro (`cliente_service.py`) está levantando uma exceção `RuntimeError` (não tratada) quando o nome do cliente contém dígitos, causando o erro 500 ao invés de um status HTTP apropriado (4xx) para uma falha de validação.

## O Que Muda?

- **Correção:** Substituir `RuntimeError` por `HTTPException(status_code=400)` na validação de nome para consistência com as demais validações de negócio (CPF e email duplicados).
- **Sem mudança em comportamento de negócio:** A regra de rejeição de nomes com dígitos permanece inalterada (decisão de produto em aberto — veja design.md).

## Capacidades

### Novas Capacidades
- `cliente-validation-error-handling` — tratamento consistente de erros de validação no registro de clientes

### Capacidades Modificadas
Nenhuma.

## Impacto

- **Código afetado:** `app/services/cliente_service.py` (método `criar_cliente`)
- **APIs afetadas:** POST /clientes
- **Dependências:** Nenhuma mudança
- **Bancos de dados:** Nenhuma mudança
- **Sistema externo:** Nenhum; o erro é interno ao backend
- **Testes:** O projeto não possui suite de testes; será necessário adicionar testes de validação para este endpoint
