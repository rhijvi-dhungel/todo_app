from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine, SessionLocal
from models import Todo

app = FastAPI()

try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Warning: Could not create database tables: {e}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GET ALL TODOS
@app.get("/todos")
def get_todos():
    db = SessionLocal()
    todos = db.query(Todo).all()
    db.close()
    return todos

# CREATE TODO
@app.post("/todos")
def create_todo(data: dict):
    db = SessionLocal()
    todo = Todo(title=data["title"], completed=False)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    db.close()
    return todo

# DELETE TODO
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    db = SessionLocal()
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    db.delete(todo)
    db.commit()
    db.close()
    return {"message": "deleted"}

# TOGGLE TODO
@app.put("/todos/{todo_id}")
def toggle_todo(todo_id: int):
    db = SessionLocal()
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    todo.completed = not todo.completed
    db.commit()
    db.refresh(todo)
    db.close()
    return todo