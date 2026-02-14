from fastapi import FastAPI
from app.routes import auth_routes, test_routes

app = FastAPI(title="Crypto Exchange - User Module")

app.include_router(auth_routes.router)
app.include_router(test_routes.router)

@app.get("/")
async def root():
    return {"message": "User Module Running Successfully"}