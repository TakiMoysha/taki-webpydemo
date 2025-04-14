from litestar import get


@get("/health")
async def health_check() -> dict:
    return {"status": "ok"}
