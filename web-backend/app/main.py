from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
import uuid
import logging

app = FastAPI(title="Event Management API")

# Setup simple logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simulating connections from environment variables (Secrets from Key Vault)
COSMOS_CONNECTION = os.getenv("COSMOS_CONNECTION_STRING", "dummy-cosmos-conn")
REDIS_CONNECTION = os.getenv("REDIS_CONNECTION_STRING", "dummy-redis-conn")
RABBITMQ_CONNECTION = os.getenv("RABBITMQ_CONNECTION_STRING", "dummy-rmq-conn")
EVENTHUB_CONNECTION = os.getenv("EVENTHUB_CONNECTION_STRING", "dummy-eh-conn")
STORAGE_CONNECTION = os.getenv("STORAGE_CONNECTION_STRING", "dummy-storage-conn")

class Event(BaseModel):
    id: Optional[str] = None
    title: str
    description: str
    date: str
    location: str

# In-memory storage for simplicity, simulating CosmosDB
db = {}

@app.on_event("startup")
async def startup_event():
    logger.info(f"Connecting to CosmosDB using: {COSMOS_CONNECTION[:10]}...")
    logger.info(f"Connecting to Redis using: {REDIS_CONNECTION[:10]}...")
    logger.info(f"Connecting to RabbitMQ using: {RABBITMQ_CONNECTION[:10]}...")
    logger.info(f"Connecting to EventHub using: {EVENTHUB_CONNECTION[:10]}...")
    logger.info(f"Connecting to Blob Storage using: {STORAGE_CONNECTION[:10]}...")

@app.get("/api/events", response_model=List[Event])
def list_events(search: Optional[str] = None):
    # Simulate Redis Cache check
    logger.info("Checking Redis cache for events...")
    
    events = list(db.values())
    if search:
        events = [e for e in events if search.lower() in e.title.lower() or search.lower() in e.description.lower()]
    return events

@app.post("/api/events", response_model=Event)
def create_event(event: Event):
    event.id = str(uuid.uuid4())
    db[event.id] = event
    
    # Simulate publishing to EventHub/RabbitMQ
    logger.info(f"Publishing event {event.id} to RabbitMQ and EventHub")
    
    return event

@app.put("/api/events/{event_id}", response_model=Event)
def update_event(event_id: str, event: Event):
    if event_id not in db:
        raise HTTPException(status_code=404, detail="Event not found")
    event.id = event_id
    db[event_id] = event
    return event

@app.delete("/api/events/{event_id}")
def delete_event(event_id: str):
    if event_id not in db:
        raise HTTPException(status_code=404, detail="Event not found")
    del db[event_id]
    return {"message": "Event deleted successfully"}
