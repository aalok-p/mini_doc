from fastapi import FastAPI

app = FastAPI(title="mini doc bookings")

@app.get("/health")
async def health():
    return {"status": "ok"}
