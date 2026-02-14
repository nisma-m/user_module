from fastapi import FastAPI

app = FastAPI(title="Crypto Exchange - User Module")

@app.get("/")
async def root():
    return {"message": "User Module Running Successfully"}