# OpenSpec Archive

| Date | Change | Jira | Summary |
|------|--------|------|---------|
| 2026-08-11 | ssai-115-post-clientes-500-error-handling | SSAI-115 | Fixed HTTP 500 errors in POST /clientes by replacing unhandled RuntimeError with HTTPException(400) for name-with-digit validation, aligning error handling with CPF and email uniqueness checks. |
