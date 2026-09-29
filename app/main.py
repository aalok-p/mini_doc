from fastapi import FastAPI
from app.routers import auth

app = FastAPI(title="mini doc bookings")
app.include_router(auth.router)

@app.get("/health")
async def health():
    return {"status": "ok"}
