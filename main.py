
from fastapi import FastAPI, status, HTTPException, Depends
from database import Base, engine
from sqlalchemy.orm import Session
from models import ModelToDo
from typing import List
from schemas import ToDoCreate, SchemaToDo

# Create the database
Base.metadata.create_all(engine)

# Initialize app
app = FastAPI()

# Helper function to get database session
def get_db():
    session = Session(bind=engine, expire_on_commit=False)
    return session

@app.get("/")
def root():
    return "Submission of Assignment(ToDo List API with FastAPI) for Wobot.ai Internship"

@app.post("/todo", response_model=SchemaToDo, status_code=status.HTTP_201_CREATED)
def create_todo(todo: ToDoCreate):

    session = get_db()
    # create an instance of the ToDo database model
    tododb = ModelToDo(task = todo.task)

    # add it to the session and commit it
    session.add(tododb)
    session.commit()
    session.refresh(tododb)

    # return the todo object
    return tododb

@app.get("/todo/{id}", response_model=SchemaToDo)
def read_todo(id: int):
    session = get_db()
    # get the todo item with the given id
    todo = session.query(ModelToDo).get(id)

    # check if todo item with given id exists. If not, raise exception and return 404 not found response
    if not todo:
        raise HTTPException(status_code=404, detail=f"Item with id {id} not found")

    return todo

@app.put("/todo/{id}", response_model=SchemaToDo)
def update_todo(id: int, task: str):

    session = get_db()
    # get the todo item with the given id
    todo = session.query(ModelToDo).get(id)

    # update todo item with the given task (if an item with the given id was found)
    if todo:
        todo.task = task
        session.commit()

    # check if todo item with given id exists, else raise exception
    if not todo:
        raise HTTPException(status_code=404, detail=f"Item with id {id} not found")

    return todo

@app.delete("/todo/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: int):

    session = get_db()
    # get the todo item with the given id
    todo = session.query(ModelToDo).get(id)

    # if todo item with given id exists, delete it from the database. Else raise exception
    if todo:
        session.delete(todo)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"Item with id {id} not found")

    return None

@app.get("/todo", response_model = List[SchemaToDo])
def read_todo_list():
    session = get_db()
    # get all todo items
    todo_list = session.query(ModelToDo).all()

    return todo_list

    

