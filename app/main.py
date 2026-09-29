from fastapi import FastAPI
from app.routers import auth, booking, payment

app = FastAPI(title="mini doc bookings")
app.include_router(auth.router)
app.include_router(booking.router)
app.include_router(payment.router)

@app.get("/health")
async def health():
    return {"status": "ok"}
