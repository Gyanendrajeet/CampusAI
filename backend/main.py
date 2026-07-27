from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from database import engine, get_db
from models import Base, User, ChatHistory, CollegeInformation

app = FastAPI()

# Frontend connection allow
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {
        "message": "CampusAI Backend Running"
    }

# Create User API
@app.post("/users")
def create_user(
    name: str,
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    try:
        user = User(
            name=name,
            email=email,
            password=password
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return {
            "message": "User created successfully",
            "user_id": user.id
        }

    except Exception as e:
        db.rollback()
        return {
            "error": str(e)
        }

# Save Chat History API
@app.post("/chat")
def save_chat(
    user_id: int,
    question: str,
    answer: str,
    db: Session = Depends(get_db)
):
    try:
        chat = ChatHistory(
            user_id=user_id,
            question=question,
            answer=answer
        )

        db.add(chat)
        db.commit()
        db.refresh(chat)

        return {
            "message": "Chat saved successfully",
            "chat_id": chat.id
        }

    except Exception as e:
        db.rollback()
        return {
            "error": str(e)
        }

# Fetch Chat History API
@app.get("/chat/{user_id}")
def get_chat_history(
    user_id: int,
    db: Session = Depends(get_db)
):
    chats = db.query(ChatHistory).filter(
        ChatHistory.user_id == user_id
    ).all()

    return [
        {
            "id": chat.id,
            "user_id": chat.user_id,
            "question": chat.question,
            "answer": chat.answer,
            "created_at": chat.created_at
        }
        for chat in chats
    ]

# Add College Information API
@app.post("/college-info")
def add_college_info(
    title: str,
    description: str,
    db: Session = Depends(get_db)
):
    try:
        college_info = CollegeInformation(
            title=title,
            description=description
        )

        db.add(college_info)
        db.commit()
        db.refresh(college_info)

        return {
            "message": "College information added successfully",
            "id": college_info.id
        }

    except Exception as e:
        db.rollback()
        return {
            "error": str(e)
        }

# Fetch College Information API
@app.get("/college-info")
def get_college_info(
    db: Session = Depends(get_db)
):
    data = db.query(CollegeInformation).all()

    return [
        {
            "id": info.id,
            "title": info.title,
            "description": info.description
        }
        for info in data
    ]