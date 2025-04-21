from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json
from typing import List, Optional
from parse import get_disciplines_module, get_url_direction
from json_transformer import create_hierarchy
from contextlib import asynccontextmanager

from database import get_faculties_db, get_roadmaps_db, get_disciplines_db, create_tables,  delete_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print('База очищена')
    await create_tables()
    print('База готова')
    yield
    print("Выключение")

app = FastAPI(lifespan=lifespan)

origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type", "Authorization", "Set-Cookie", "Access-Control-Allow-Origin", "Access-Control-Allow-Headers"],
)

class Subject(BaseModel):
    name: str

class Department(BaseModel):
    id: str
    title: str
    # directions: List[Subject]

class Faculties(BaseModel):
    data: List[Department]

# def load_faculties_data():
#     script_dir = os.path.dirname(os.path.abspath(__file__))
#     file_path = os.path.join(script_dir, "faculties.json")
#     with open(file_path, 'r', encoding='utf-8') as file:
#         return json.load(file)


@app.get("/api/faculties/")
async def get_faculties() -> Faculties:
    data = await get_faculties_db()
    modified_data = [
        {"id": faculty["id"], "title": faculty["title"]}
        for faculty in data["data"]
    ]
    return {"data": modified_data}

@app.get("/api/faculties/{faculty_id}")
async def get_faculty_id(faculty_id: str):
    data = await get_faculties_db()
    
    # Ищем факультет по ID
    faculty = next(
        (f for f in data["data"] if f["id"] == faculty_id),
        None
    )
    
    if not faculty:
        raise HTTPException(status_code=404, detail="Факультет не найден")
    
    return faculty


@app.get("/api/roadmaps/{discipline}/{link_id}")
async def get_roadmaps(discipline: str, link_id:str) -> object:
    data = await get_roadmaps_db(discipline, link_id)
    return data


@app.get("/api/get_disciplines/{direction}")
async def get_disciplines(direction: str) -> object:
    data = await get_disciplines_db(direction)
    return data

