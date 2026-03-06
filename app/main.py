from fastapi import FastAPI
from app.core.configs import settings
from app.core.database import engine
from app.models.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="API do Case Sensedia - Gestão de Clientes e Apólices"
)

@app.get("/")
def home():
    return {"msg": "O servidor está rodando e o banco foi conectado!"}