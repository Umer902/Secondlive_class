from fastapi import FastAPI
from sqlmodel import SQLModel, Field, create_engine, Session
from contextlib import asynccontextmanager
from secondlive_class import setting

# Step 1: Define Database Table Schema
class Todo(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str

# Step 2: Create Database Engine
connection_str = str(setting.DATABASE_URL).replace(
     "postgresql", "postgresql+psycopg"
)
engine = create_engine(connection_str)

# Step 3: Create Database Tables
def create_db_tables():
    print("create_db_tables")
    SQLModel.metadata.create_all(engine)
    print("done")

@asynccontextmanager
async def lifespan(todo_server: FastAPI):
    print("Server Startup")
    create_db_tables()
    yield
# Create FastAPI app
app = FastAPI(lifespan=lifespan)

# Step 5: Define API Endpoints
@app.get("/")
def read_root():
    return ("Assalamoalikum, FastAPI")

@app.get("/city")
def read_city():
    return ("City: Faisalabad")

@app.post("/todos")
def create_todo(todo: Todo):
    with Session(engine) as session:
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo
