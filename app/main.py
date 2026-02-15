from fastapi import FastAPI
from app.routes.fiat_routes import router as fiat_router
from app.routes.websocket_routes import router as ws_router

app = FastAPI()

app.include_router(fiat_router, prefix="/fiat", tags=["Fiat"])
app.include_router(ws_router)   # IMPORTANT

@app.get("/")
async def root():
    return {"message": "Running"}
