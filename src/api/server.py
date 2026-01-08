from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import Routers
from src.api.routes import analytics_router

# App Configuration
app = FastAPI(
    title="Aevo Deep Fetch Analytics API",
    description="API to extract, process, and analyze innovation data from Aevo.",
    version="1.0.0"
)

# CORS (Allow frontend to access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routes
app.include_router(analytics_router.router)

@app.get("/")
def health_check():
    return {"status": "running", "message": "Welcome to Aevo Deep Fetch API. Go to /docs for Swagger."}

# Entry point for running directly
if __name__ == "__main__":
    # Reload=True allows auto-restart when you change code
    uvicorn.run("src.api.server:app", host="0.0.0.0", port=8000, reload=True)