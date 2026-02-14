from fastapi import FastAPI
from app.routes import auth_routes

app = FastAPI(title="Crypto Exchange - User Module")

app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])

@app.get("/")
async def root():
    return {"message": "User Module Running Successfully"}
