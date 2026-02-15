from fastapi import FastAPI
from app.routes.fiat_routes import router as fiat_router
from app.routes.websocket_routes import router as ws_router
from app.routes import auth_routes, wallet_routes, test_routes

app = FastAPI()

# Auth + Wallet (mem1 + mem2)
app.include_router(auth_routes.router)
app.include_router(wallet_routes.router)

# Fiat + Websocket
app.include_router(fiat_router, prefix="/fiat", tags=["Fiat"])
app.include_router(ws_router)

# Test routes
app.include_router(test_routes.router)


@app.get("/")
async def root():
    return {"message": "Running"}
