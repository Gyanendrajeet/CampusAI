from fastapi import FastAPI
from routes import chat
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

app.include_router(chat.router)

@app.get("/")
def home():
    return {"message": "CampusAI Backend Running"}
