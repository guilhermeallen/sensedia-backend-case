from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.log_service import LogService
from app.schemas.schemas import LogErroResponse


router = APIRouter(prefix="/logs", tags=["Logs"])


@router.get("", response_model=List[LogErroResponse])
def buscar_logs(
    data_inicio: Optional[datetime] = Query(None, description="Filtra logs a partir desta data (inclusive). Ex: 2025-01-01T00:00:00"),
    data_fim: Optional[datetime] = Query(None, description="Filtra logs até esta data (inclusive). Ex: 2025-01-31T23:59:59"),
    level: Optional[str] = Query(None, description="Filtra por level (ex: ERROR, WARNING)"),
    status_code: Optional[int] = Query(None, description="Filtra por status code HTTP (ex: 500, 404)"),
    db: Session = Depends(get_db),
):
    service = LogService(db)
    return service.buscar_logs(
        data_inicio=data_inicio,
        data_fim=data_fim,
        level=level,
        status_code=status_code,
    )
