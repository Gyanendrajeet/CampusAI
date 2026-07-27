from fastapi import APIRouter

router = APIRouter()

@router.post("/chat")
def chat(message: str):
    return {
        "user_message": message,
        "bot_response": "CampusAI is ready!"
    }