from fastapi import FastAPI
from starlette import status
import databases, sqlalchemy
from pydantic import BaseModel, Field
from typing import List

app = FastAPI()

@app.on_event("startup")
async def startyup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

DATABASE_URL="postgresql://postgres:6282@127.0.0.1:5433/postgres"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()



classes = sqlalchemy.Table(
    "classes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("name", sqlalchemy.String)
)
week = sqlalchemy.Table(
    "week",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("name", sqlalchemy.String)
)
teacher = sqlalchemy.Table(
    "teacher",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("speciality", sqlalchemy.String)
)
cabinet = sqlalchemy.Table(
    "cabinet",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("name", sqlalchemy.String)
)
timetable = sqlalchemy.Table(
    "timetable",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("id_class", sqlalchemy.Integer),
    sqlalchemy.Column("id_week", sqlalchemy.Integer)
)

lesson = sqlalchemy.Table(
    "lesson",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("start_time", sqlalchemy.String),
    sqlalchemy.Column("end_time", sqlalchemy.String),
    sqlalchemy.Column("name_1", sqlalchemy.String),
    sqlalchemy.Column("id_cabinet_1", sqlalchemy.Integer),
    sqlalchemy.Column("id_teacher_1", sqlalchemy.Integer),
    sqlalchemy.Column("have_second_group", sqlalchemy.Boolean),
    sqlalchemy.Column("name_2", sqlalchemy.String),
    sqlalchemy.Column("id_cabinet_2", sqlalchemy.Integer),
    sqlalchemy.Column("id_teacher_2", sqlalchemy.Integer),
    sqlalchemy.Column("id_timetable", sqlalchemy.Integer)

)

engine = sqlalchemy.create_engine(
    DATABASE_URL
)
metadata.create_all(engine)

class Classes(BaseModel):
    id:int
    name:str

class Week(BaseModel):
    id:int
    name:str

class Timetable(BaseModel):
    id:int
    id_class:int
    id_week:int


class TeacherList(BaseModel):
    id:int
    name:str
    speciality:str

class TeacherEntry(BaseModel):
    name:str
    speciality:str

class TimetableClassList(BaseModel):
    name_class: str
    name_week: str
    start_time: str
    end_time: str
    name_1: str
    teacher_name_1:str
    cabinet_name_1:str
    name_2: str
    teacher_name_2:str
    cabinet_name_2:str


@app.get("/", status_code=status.HTTP_404_NOT_FOUND)
async def read_root():
    #  response.status_code=status.HTTP_404_NOT_FOUND
    return "NOT_FOUND"

@app.get("/teachers_list", response_model=List[TeacherList])
async def find_all_teachers():
    query = teacher.select()
    return await database.fetch_all(query)

@app.get("/timetable_class_list")
async def get_timetable_class(class_id: int, week_id: int):
    query = f"SELECT * FROM timetable WHERE id_class = '{class_id}' AND id_week = '{week_id}'"
    test = await database.fetch_all(query)
    if test:
        query = f"SELECT * FROM lesson WHERE id_timetable = '{test[0]['id']}'"
        return await database.fetch_all(query)
    else:
        return None

@app.get("/teacher_info")
async def teacher_info(teacher_id: int):
    query = f"SELECT * FROM teacher WHERE id = '{teacher_id}'"
    return await database.fetch_one(query)

@app.get("/classes_info")
async def classes_info(class_name: str):
    query = f"SELECT * FROM classes WHERE name = '{class_name}'"
    return await database.fetch_one(query)

@app.get("/cabinet_info")
async def cabinet_info(cabinet_id: int):
    query = f"SELECT * FROM cabinet WHERE id = '{cabinet_id}'"
    return await database.fetch_one(query)

@app.post("/add_teacher")
async def add_teacher(teacher_name: str, teacher_speciality: str):
    query = f"INSERT INTO teacher(name,speciality) VALUES('{teacher_name}', '{teacher_speciality}')"
    await database.execute(query)
    return "ok"

@app.post("/add_cabinet")
async def add_cabinet(cabinet_name: str):
    query = f"INSERT INTO cabinet(name) VALUES('{cabinet_name}')"
    await database.execute(query)
    return "ok"

@app.post("/add_classes")
async def add_classes(class_name: str):
    query = f"INSERT INTO classes(name) VALUES('{class_name}')"
    await database.execute(query)
    return "ok"

@app.post("/add_timetable")
async def add_timetable(id_week: int, name_class: str):
    a = await classes_info(name_class)
    if a:
        id_class = a[0]
        query = f"INSERT INTO timetable(id_class, id_week) VALUES('{id_class}', '{id_week}')"
        await database.execute(query)
        return "ok"
    else:
        return None

@app.post("/add_lesson")
async def add_classes(start_time:str, end_time: str, name_1: str, id_cabinet_1:int, id_teacher_1:int, id_timetable:int, have_second_group:bool, name_2:str = None, id_cabinet_2:int = 0, id_teacher_2:int = 0):
    query = f"INSERT INTO lesson(start_time,end_time,name_1,id_cabinet_1,id_teacher_1,have_second_group,name_2,id_cabinet_2,id_teacher_2,id_timetable) VALUES('{start_time}','{end_time}','{name_1}','{id_cabinet_1}','{id_teacher_1}','{have_second_group}','{name_2}','{id_cabinet_2}','{id_teacher_2}','{id_timetable}')"
    await database.execute(query)
    return "ok"