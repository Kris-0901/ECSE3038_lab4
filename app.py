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