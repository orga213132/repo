from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from repositories.users import *
from typing import List
from bson import ObjectId

from models.user import User
from models.base import ResponseModel, ErrorResponseModel

router = APIRouter()

@router.post("/", response_description="User data added into the database")
async def add_user_data(user: User = Body(...)):
    user = jsonable_encoder(user)
    new_user = await add_user(user)
    return ResponseModel(new_user, "User added successfully.")

@router.get('/', response_model=List[User])
async def get_users():
    return await retrieve_users()

@router.get('/{id}', response_model=User)
async def get_user_by_id(id: int):
    return await retrieve_user_by_steam_id(id=id)

@router.delete('/{id}', response_model=bool)
async def delete_user(id: int):
    return await delete_user_by_id(id=id)

@router.patch('/{id}', response_model=User)
async def update_user(id: int):
    new_user = await update_user_by_steam_id(id=id)
    return new_user

@router.patch('/', response_model=bool)
async def update_users():
    return await update_user_line()