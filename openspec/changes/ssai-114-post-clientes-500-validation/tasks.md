# Tarefas de Implementação — SSAI-114

## 1. Correção da Validação

- [ ] 1.1 Alterar `app/services/cliente_service.py` para levantar `HTTPException(status_code=400)` ao invés de `RuntimeError` quando o nome contém dígitos
- [ ] 1.2 Garantir que a mensagem de erro seja descritiva e em português

## 2. Testes de Validação

- [ ] 2.1 Criar arquivo de testes `tests/services/test_cliente_service.py` com testes para o método `criar_cliente()`
- [ ] 2.2 Adicionar teste: criar cliente com nome válido (sem dígitos) deve retornar sucesso
- [ ] 2.3 Adicionar teste: criar cliente com nome contendo dígitos deve retornar HTTP 400
- [ ] 2.4 Adicionar teste: criar cliente com CPF duplicado deve retornar HTTP 400
- [ ] 2.5 Adicionar teste: criar cliente com email duplicado deve retornar HTTP 400

## 3. Testes de Integração (Router)

- [ ] 3.1 Criar arquivo de testes `tests/routers/test_cliente_router.py` com testes de POST /clientes
- [ ] 3.2 Adicionar teste: POST /clientes com nome válido retorna HTTP 201 Created
- [ ] 3.3 Adicionar teste: POST /clientes com nome contendo dígitos retorna HTTP 400 (não 500)
- [ ] 3.4 Adicionar teste: POST /clientes com CPF duplicado retorna HTTP 400
- [ ] 3.5 Adicionar teste: POST /clientes com email duplicado retorna HTTP 400

## 4. Verificação

- [ ] 4.1 Executar testes localmente e validar que todos passam
- [ ] 4.2 Executar linter (se disponível) e garantir conformidade
- [ ] 4.3 Verificar que a correção resolve o problema descrito no alerta (POST /clientes com nome com dígitos agora retorna 400, não 500)
