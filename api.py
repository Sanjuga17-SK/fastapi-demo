from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# connect database
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

# create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER
)
""")
conn.commit()



# create data model
class User(BaseModel):
    name: str
    age: int

# GET API with input
@app.get("/student/{student_id}")
def get_student(student_id: int):

    return {
        "student_id": student_id,
        "name": "Sanjuga",
        "status": "Active"
    }

@app.get("/square/{square_id}")
def get_square(square_id: int):

    return{
        "square_id":square_id*5,
        "name": "square"
    }


# POST API
@app.post("/add_user1")
def add_user1(user1: User):

    return {
        "message": "User added successfully",
        "name": user1.name,
        "age": user1.age
    }


# POST API save to database
@app.post("/add_user")
def add_user(user: User):

    cursor.execute(
        "INSERT INTO users (name, age) VALUES (?, ?)",
        (user.name, user.age)
    )

    conn.commit()

    return {
        "message": "User saved in database"
    }

# GET API fetch users
@app.get("/users")
def get_users():

    cursor.execute("SELECT * FROM users")

    data = cursor.fetchall()

    return {
        "users": data
    }