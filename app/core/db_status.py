import threading
import time

from sqlalchemy import text

from app.core.database import engine


_lock = threading.Lock()
_last_check = 0.0
_last_result = False
_CACHE_SECONDS = 5.0


def banco_disponivel() -> bool:
    """Verifica se o banco de dados está acessível, com cache curto para evitar
    latência em rajadas de requisições."""
    global _last_check, _last_result

    with _lock:
        if time.time() - _last_check < _CACHE_SECONDS:
            return _last_result

        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            _last_result = True
        except Exception:
            _last_result = False
        finally:
            _last_check = time.time()

        return _last_result
