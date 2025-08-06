from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from api.routes import router

app = FastAPI(
    title="LLM Document Query System",
    version="0.1.0"
)

# Register API routes
app.include_router(router, prefix="/api/v1")

# Global exception handler to catch internal server errors
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": str(exc)
        }
    )
