import uuid
import time
from fastapi import FastAPI, Request
from app.core.configs import settings
from app.core.database import engine
from app.models.models import Base
from app.routers import cliente_router
from app.routers import cliente_router, apolice_router

#Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="API do Case Sensedia - Gestão de Clientes e Apólices"
)


# --- REQUISITO: LOGS E CORRELATION ID  ---
@app.middleware("http")
async def add_correlation_id(request: Request, call_next):
    # 1. Gera um ID único para a requisição
    correlation_id = str(uuid.uuid4())
    
    # 2. Adiciona no log (print simples aparece no log do Render)
    print(f"[{correlation_id}] Iniciando requisição: {request.method} {request.url}")
    
    start_time = time.time()
    
    # 3. Processa a requisição
    response = await call_next(request)
    
    # 4. Calcula tempo de execução
    process_time = time.time() - start_time
    
    # 5. Adiciona o ID no header da resposta (útil para debug no Postman)
    response.headers["X-Correlation-ID"] = correlation_id
    
    print(f"[{correlation_id}] Finalizado em {process_time:.4f}s - Status: {response.status_code}")
    
    return response


app.include_router(cliente_router.router, prefix=settings.API_V1_STR)
app.include_router(apolice_router.router, prefix=settings.API_V1_STR)

@app.get("/")
def home():
    return {"msg": "O servidor está rodando e o banco foi conectado!"}