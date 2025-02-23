from fastapi import FastAPI,HTTPException,status
from fastapi.encoders import jsonable_encoder
import motor.motor_asyncio
from pydantic import BaseModel, BeforeValidator, Field
from typing import Annotated, List
from bson import ObjectId
from pymongo import ReturnDocument
from fastapi.responses import Response, JSONResponse
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

class TankCollection(BaseModel):
    all_tanks: List[Tank]

class Tank_Update(BaseModel):
    location:str | None = None
    lat:float | None = None
    long:float | None = None

@app.get("/profile")
async def get_profile():
    number_of_profiles = await profile.count_documents({})
    profile_collection = await profile.find_one({})

    if number_of_profiles > 0:
        profile_format = Profile(**profile_collection)
        #print(profile_format)

        profile_json = jsonable_encoder(profile_format)

        return JSONResponse(profile_json,status_code=200)
    
    return JSONResponse({},status_code=200)

@app.post("/profile",status_code=status.HTTP_201_CREATED)
async def create_profile(new_profile:Profile):
   
    # check for an exixting profile
    number_of_profiles = await profile.count_documents({})
    # print (number_of_profiles)

    if number_of_profiles < 1:
        # post the profile if no profile exists
        profile_dict = new_profile.model_dump(exclude=["id"])
        created_profile = await profile.insert_one(profile_dict)

        newly_created_profile = await profile.find_one({"_id":created_profile.inserted_id})
    else: 
        raise HTTPException(status_code = 409, detail = "Profile already exisits")
    

    profile_format = Profile(**newly_created_profile)
    #print(profile_format)

    profile_json = jsonable_encoder(profile_format)

    return JSONResponse(profile_json,status_code=201)

@app.get("/tank")
async def get_all_tanks():
    tank_collection = await tanks.find().to_list(1001)

    tanks_list = []

    for tank in tank_collection:
        tanks_list.append(Tank(**tank))

    tanks_list_json = jsonable_encoder(tanks_list)
    
    return JSONResponse(tanks_list_json,status_code=200)

@app.post ("/tank",status_code=status.HTTP_201_CREATED)
async def add_tank(new_tank:Tank):
    tank_dict = new_tank.model_dump(exclude=["id"])
    created_tank = await tanks.insert_one(tank_dict)

    newly_created_tank = await tanks.find_one({"_id":created_tank.inserted_id})

    timestamp = datetime.now(ZoneInfo('America/Jamaica'))
    timestamp_formatted = timestamp.strftime("%B %d,%Y %I:%M %p %Z")

    await profile.update_one({},{'$set':{'last_updated':timestamp_formatted}})

    tank_format = Tank(**newly_created_tank)

    tank_json =jsonable_encoder(tank_format)

    return JSONResponse(tank_json,status_code=201)

@app.patch("/tank/{id}",response_model=Tank,status_code=status.HTTP_200_OK)
async def update_tank(id:str, updated_tank:Tank_Update):
    tank_update_dict = updated_tank.model_dump(exclude_unset=True)

    new_updated_tank = await tanks.find_one_and_update(
        {'_id': ObjectId(id)},
        {'$set': tank_update_dict},
        return_document=ReturnDocument.AFTER
    )

    if new_updated_tank is not None:

        timestamp = datetime.now(ZoneInfo('America/Jamaica'))
        timestamp_formatted = timestamp.strftime("%B %d,%Y %I:%M %p %Z")

        await profile.update_one({},{'$set':{'last_updated':timestamp_formatted}})

        return new_updated_tank
    
    else:
        raise HTTPException(status_code=404,detail=f"Tank wit id: '{id}' not found")
    
@app.delete("/tank/{id}")
async def delete_tank(id: str):
    delete_tank_result= await tanks.delete_one({'_id':ObjectId(id)})

    if delete_tank_result.deleted_count == 1:

        timestamp = datetime.now(ZoneInfo('America/Jamaica'))
        timestamp_formatted = timestamp.strftime("%B %d,%Y %I:%M %p %Z")

        await profile.update_one({},{'$set':{'last_updated':timestamp_formatted}})

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    raise HTTPException(status_code=404, detail=f"Tank with id: '{id}' not found")
