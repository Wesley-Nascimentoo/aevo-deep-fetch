from fastapi import FastAPI
from src.controllers.ideas_controller import router as ideas_router
from src.controllers.user_per_dep_controller import router as users_router

app = FastAPI(
    title="Aevo DeepFetch Middleware",
    description="API intermediária para busca e tratamento de dados da Aevo Innovate.",
    version="1.0.0"
)

app.include_router(ideas_router, prefix="/ideias", tags=["Ideias"])

app.include_router(users_router, prefix="/usuarios", tags=["Usuários"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)



