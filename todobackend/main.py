from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine, SessionLocal
from models import Todo

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# CORS (frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GET ALL TODOS
@app.get("/todos")
def get_todos(db: Session = Depends(get_db)):
    return db.query(Todo).all()

# CREATE TODO
@app.post("/todos")
def create_todo(todo: dict, db: Session = Depends(get_db)):
    new_todo = Todo(title=todo["title"], completed=False)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

# DELETE TODO
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo)
    db.commit()
    return {"message": "deleted"}

# TOGGLE TODO
@app.put("/todos/{todo_id}")
def toggle_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo.completed = not todo.completed
    db.commit()
    db.refresh(todo)
    return todo