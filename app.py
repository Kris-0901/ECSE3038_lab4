from fastapi import FastAPI,HTTPException,status
from fastapi.encoders import jsonable_encoder
import motor.motor_asyncio
from pydantic import BaseModel, BeforeValidator, Field
from typing import Annotated, List
from bson import ObjectId
from pymongo import ReturnDocument
from fastapi.responses import Response
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime,timedelta
from zoneinfo import ZoneInfo,available_timezones

#print(available_timezones())
timestamp = datetime.now(ZoneInfo('America/Jamaica'))
timestamp_formatted = timestamp.strftime("%B %d,%Y %I:%M %p %Z")


origins = [ "https://ecse3038-lab3-tester.netlify.app" ]


load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

connection = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGODB_URL"))
db = connection.iot_water_tanks
profile = db.profile
tanks = db.tanks

PyObjectId = Annotated[str, BeforeValidator(str)] # ID for MongoDB


class Profile(BaseModel):
    id: PyObjectId | None = Field(default=None, alias="_id")
    last_updated:str = timestamp_formatted
    username: str
    role: str
    color: str

class ProfileCollection(BaseModel):
    profiles: List[Profile]


class Tank(BaseModel):
    id: PyObjectId | None = Field(default=None, alias="_id")
    location: str
    lat: float
    long: float

class Tank_Update(BaseModel):
    location:str | None = None
    lat:float | None = None
    long:float | None = None

@app.get("/profile")
async def get_profile():
    profile_collection = await profile.find().to_list(2)

    return ProfileCollection(profiles=profile_collection)

@app.post("/profile",status_code=status.HTTP_201_CREATED)
async def create_profile(new_profile:Profile):
    profile_dict=new_profile.model_dump(exclude=["id"])
    created_profile = await profile.insert_one(profile_dict)

    profiles = await profile.find_one({"_id":created_profile.inserted_id})

    return Profile(**profiles)