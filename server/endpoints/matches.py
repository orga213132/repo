from fastapi import APIRouter, Body
from models.matches import Match
from models.base import ResponseModel, ErrorResponseModel
from repositories.matches import *
from fastapi.encoders import jsonable_encoder

router = APIRouter()

@router.post('/')
async def create_match(match: Match):
    print(match)
    match = jsonable_encoder(match)
    new_match = await add_match(match=match)
    if new_match:
        return new_match
    else:
        return ErrorResponseModel(message='Not able to add a new match')

@router.delete('/{id}')
async def delete(id: str):
    return await delete_match(id=id)

@router.get('/{id}', response_model=list)
async def get_by_steamid(id: int):
    return await retrieve_by_steamid(id=id)