from fastapi import FastAPI
from backend.services import scrape_service, listings_service, notify_service

app = FastAPI()

@app.get("/scrape")
def scrape():
    return scrape_service()

@app.get("/listings")
def listings():
    return listings_service()

@app.post("/send_email")
def send_email():
    return notify_service()
