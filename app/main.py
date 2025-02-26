from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.database.database import init_db
from app.exceptions import (database_exception_handler,
                            global_exception_handler, http_exception_handler)
from app.routers.user_routers import router
from app.utils.logger import logger

app = FastAPI()

#  Register exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(SQLAlchemyError, database_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)
# Include user routes
app.include_router(router)

init_db()
logger.info("Application started")


@app.get("/")
def home():
    return {"message": "FastAPI connected to PostgreSQL!"}
