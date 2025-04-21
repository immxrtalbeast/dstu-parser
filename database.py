from motor.motor_asyncio import AsyncIOMotorClient
import json
import os
from parse import get_disciplines_module, get_url_direction
from json_transformer import create_hierarchy

# Подключение к базе данных planedu
client = AsyncIOMotorClient("mongodb://mongo-parser:27017") #client = MongoClient("localhost", 27017)("mongodb://mongo-parser:27017")

db = client.planedu

async def create_tables():
    # Mongo не требует явного создания коллекций — они создаются при первом обращении
    pass

async def delete_tables():
    await db.faculties.drop()
    await db.roadmaps.drop()
    await db.disciplines.drop()
    print("Коллекции удалены")

async def get_faculties_db():
    faculties = db.faculties
    data = await faculties.find_one({"table": 1})
    if data:
        return data['faculties']
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, "faculties.json")
        with open(file_path, 'r', encoding='utf-8') as file:
            test = json.load(file)
        await faculties.insert_one({"faculties": test, "table": 1})
        data = await faculties.find_one({"table": 1})
        return data['faculties']

async def get_roadmaps_db(discipline: str, link_id: str):
    roadmaps = db.roadmaps
    try:
        doc = await roadmaps.find_one({"table": 2})
        return doc["roadmaps"][discipline]
    except:
        await set_roadmap_db(discipline, link_id)
        doc = await roadmaps.find_one({"table": 2})
        return doc["roadmaps"][discipline]

async def set_roadmap_db(discipline_name: str, link_id: str):
    roadmaps = db.roadmaps
    data = await create_hierarchy(discipline_name, link_id)
    doc = await roadmaps.find_one({"table": 2})
    if doc:
        await update_one_roadmap(discipline_name, data)
    else:
        await roadmaps.insert_one({"roadmaps": data, "table": 2})

async def update_one_roadmap(discipline: str, data):
    roadmaps = db.roadmaps
    await roadmaps.update_one(
        {"table": 2},
        {"$set": {f"roadmaps.{discipline}": data[discipline]}}
    )

async def get_disciplines_db(direction: str):
    disciplines = db.disciplines
    try:
        doc = await disciplines.find_one({"table": 1})
        return doc["disciplines"][direction]
    except:
        await set_disciplines_db(get_url_direction(direction), direction)
        doc = await disciplines.find_one({"table": 1})
        return doc["disciplines"][direction]

async def set_disciplines_db(url: str, direction: str):
    disciplines = db.disciplines
    data_json = await get_disciplines_module(url, direction)
    doc = await disciplines.find_one({"table": 1})
    if doc:
        await update_one_discipline(direction, data_json[direction])
    else:
        await disciplines.insert_one({"disciplines": data_json, "table": 1})

async def update_one_discipline(direction: str, data):
    disciplines = db.disciplines
    await disciplines.update_one(
        {"table": 1},
        {"$set": {f"disciplines.{direction}": data}}
    )
