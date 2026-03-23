import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./zoo.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)


class AnimalDB(Base):
    __tablename__ = "animals"
    id = Column(Integer, primary_key=True, index=True)
    species = Column(String)
    name = Column(String)


Base.metadata.create_all(bind=engine)


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(..., min_length=8)


class AnimalSchema(BaseModel):
    species: str
    name: str


app = FastAPI(title="Zoo API")


@app.post("/register")
def register_user(user: UserCreate):
    db = SessionLocal()
    try:
        existing_user = (
            db.query(UserDB).filter(UserDB.username == user.username).first()
        )
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already taken")
        new_user = UserDB(
            username=user.username, email=user.email, password=user.password
        )
        db.add(new_user)
        db.commit()
        return {"message": f"User {user.username} created!"}
    finally:
        db.close()


@app.get("/animals")
def list_animals():
    return {"message": "Здесь будет список животных из БД"}


@app.put("/animals/{animal_id}")
def update_animal(animal_id: int, new_data: AnimalSchema):
    return {"message": f"Animal with id {animal_id} would be updated"}


@app.delete("/animals/{animal_id}")
def remove_animal(animal_id: int):
    return {"message": f"Animal with id {animal_id} would be deleted"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
