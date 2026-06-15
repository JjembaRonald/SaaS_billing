from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_db_and_tables
from models import Plan  # here iam  ensuring SQLModel registers the table

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Triggers automatically when you run uvicorn main:app
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"status": "SaaS Billing Engine API is running"}
