import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

animals_db = []

app = FastAPI(title="Zoo API")

class Animal(BaseModel):
    id: int
    species: str
    name: str


@app.get("/animals")
def list_animals():
    return animals_db


@app.post("/animals")
def add_animal(species: str | None = None, name: str | None = None):
    if not species:
        return {"error": "Species is required"}
    if not name:
        return {"error": "Name is required"}

    new_id = 1 if not animals_db else animals_db[-1].id + 1
    animal = Animal.model_validate({"id": new_id, "species": species, "name": name})
    animals_db.append(animal)
    return {"message": "Animal successfully added!"}


@app.put("/animals/{animal_id}")
def update_animal(animal_id: int, new_data: Animal):
    return {"message": f"Animal with id {animal_id} would be updated"}


@app.delete("/animals/{animal_id}")
def remove_animal(animal_id: int):
    return {"message": f"Animal with id {animal_id} would be deleted"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)