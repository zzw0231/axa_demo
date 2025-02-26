import traceback

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.utils.logger import logger


# Handle HTTP exceptions (e.g., 404 Not Found, 400 Bad Request)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"HTTP {exc.status_code}: {exc.detail} | Path: {request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code},
    )


# Handle Database Errors (SQLAlchemy)
async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    logger.error(f"Database Error: {str(exc)} | Path: {request.url.path}")
    return JSONResponse(
        status_code=500,
        content={"error": "Database error occurred", "status_code": 500},
    )


# Handle All Other Unexpected Exceptions
async def global_exception_handler(request: Request, exc: Exception):
    error_details = traceback.format_exc()  # Get full stack trace
    logger.critical(
        f"Unhandled Exception: {str(exc)} | Path: {request.url.path}\n{error_details}"
    )
    return JSONResponse(
        status_code=500, content={"error": "Internal Server Error", "status_code": 500}
    )
