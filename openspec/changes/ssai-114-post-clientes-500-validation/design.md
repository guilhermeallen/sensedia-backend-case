# Design — Tratamento de Erros de Validação no Registro de Clientes

## Contexto

O alerta agentico que gerou o card SSAI-114 analisou traces de requisições POST /clientes que retornavam HTTP 500. A análise identificou que o backend levantava uma exceção não tratada (`RuntimeError`) durante a validação do campo `nome`.

No código atual (`app/services/cliente_service.py`), a função `criar_cliente()` contém três validações:

```python
# Validação 1: Nome não pode conter dígitos
if re.search(r'\d', dados_cliente.nome):
    raise RuntimeError(...)  # <-- DEFECT: não tratada, vira 500

# Validação 2: CPF duplicado
if self.repository.buscar_por_cpf(dados_cliente.cpf):
    raise HTTPException(status_code=400, ...)  # <-- CORRETO

# Validação 3: Email duplicado
if self.repository.buscar_por_email(dados_cliente.email):
    raise HTTPException(status_code=400, ...)  # <-- CORRETO
```

As validações 2 e 3 usam `HTTPException(status_code=400)`, que FastAPI captura e converte em HTTP 400. A validação 1 levanta `RuntimeError` sem tratamento, que FastAPI captura como HTTP 500.

## Objetivos

1. **Objetivo primário:** Corrigir o tipo de exceção na validação de nome de modo que POST /clientes retorne HTTP 400 (não 500) quando a validação falhar
2. **Objetivo secundário:** Garantir consistência nas respostas de erro — todas as validações de negócio retornam o mesmo status HTTP

## Não-Objetivos

- Remover ou ativar a regra de rejeição de nomes com dígitos (decisão de produto — veja Decisão 1)
- Adicionar novas validações de cliente

## Decisões

### Decisão 1: Mantém a regra de validação de nome como está (não muda de comportamento)

**Escolha:** A regra que rejeita nomes contendo dígitos permanece ativa. Apenas o tipo de exceção muda, de `RuntimeError` para `HTTPException(status_code=400)`.

**Rationale:**
- A regra está no código atual e não há evidência no card indicando que deve ser removida
- Remover validações é uma mudança de negócio de maior impacto (blast radius maior)
- A correção de tipo de exceção é uma correção técnica clara contra a convenção da mesma função

## Questões Abertas

### Questão 1: A regra de "nomes com dígitos são rejeitados" é um requisito real de negócio?

**Evidência a favor:** 
- Está no código há tempo, portanto foi uma decisão consciente

**Evidência contra:**
- O card agentico menciona como "possível causa" e "recomendação", não como requisito confirmado
- Nenhum comentário no código explica por quê
- Muitos sistemas de CRM legítimos aceitam nomes com números (ex: "José 2º Silva", "Ana Maria III")

**Recomendação:** Manter por enquanto. Se for política de negócio, foi documentada; se for bugfix técnico, pode ser revisado em outra issue.

**Decisão para APPROVAL 1:** Humano confirma ou refuta na spec review.

## Riscos

### [Risk] A regra de rejeição de nome com dígitos é uma restrição muito forte
**Mitigação:** Questão aberta acima; será decidida em APPROVAL 1.

### [Risk] Nenhuma suite de testes existe no projeto
**Mitigação:** Este change adicionará testes para validação de cliente (veja tasks.md).
