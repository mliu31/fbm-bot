import sys
import asyncio

# Ensure subprocess support on Windows for Playwright under Uvicorn/asyncio
if sys.platform.startswith("win"):
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    except Exception:
        pass

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from backend.services import all_listings_service, pending_listings_service, scrape_service, notify_service
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

@app.post("/scrape")
def scrape():
    result = scrape_service()
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)

@app.get("/pending_listings")
def pending_listings():
    result = pending_listings_service()
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)

@app.get("/all_listings")
def all_listings():
    result = all_listings_service()
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)

@app.post("/send_email")
def send_email():
    result = notify_service()
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)
