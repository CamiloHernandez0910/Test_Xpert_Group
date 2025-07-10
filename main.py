from fastapi import FastAPI
from app.routes.cat.cat_routes import router as cat_router
from app.routes.user.user_routes import router as user_router

app = FastAPI(
    title="Test Xpert Group API",
    version="1.0.0",
    description="API para gestión de gatos y usuarios con autenticación JWT",
)

app.include_router(cat_router)
app.include_router(user_router)
