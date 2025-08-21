# app/main.py

from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes import user_routes, book_routes, borrow_routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    print("Starting Library API...")
    yield
    # Shutdown code
    print("Shutting down Library API...")

app = FastAPI(
    title="Library Management System API",
    description="A simple backend API for managing library books and users.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",  # Disable ReDoc
)

# Include routers
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(book_routes.router, prefix="/books", tags=["Books"])
app.include_router(borrow_routes.router, prefix="/borrow", tags=["Borrow/Return"])

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Library Management System API!"}

# If you want to run this with: `python -m app.main`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)