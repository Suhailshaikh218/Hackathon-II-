from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Ye line zaroori hai
from src.api.routes.tasks import router as task_router
from src.api.routes.auth import router as auth_router
from src.database import create_db_and_tables

app = FastAPI(
    title="Todo Task Management API",
    description="Core task management system with CRUD operations",
    version="1.0.0"
)

# --- CORS SETTINGS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 
    allow_credentials=True,
    allow_methods=["*"],  # 
    allow_headers=["*"],
)
# -------------------------------------

# Include the task and auth routes
app.include_router(task_router)
app.include_router(auth_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo Task Management API"}

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
