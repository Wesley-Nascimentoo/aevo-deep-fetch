from fastapi import FastAPI
from src.controllers.ideas_controller import router as ideas_router

app = FastAPI(
    title="Aevo DeepFetch Middleware",
    description="API intermediária para busca e tratamento de dados da Aevo Innovate.",
    version="1.0.0"
)

app.include_router(ideas_router, prefix="/ideias", tags=["Ideias"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)



