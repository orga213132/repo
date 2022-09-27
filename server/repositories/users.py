import requests
from db.base import user_collection, user_helper, user_line_collection
from bson import ObjectId
from .matches import update_last20
from core.config import headers
import json
from models.user import User

# Retrieve all students present in the database
async def retrieve_users():
    users = []
    async for user in user_collection.find():
        users.append(user)
    return users


# Add a new student into to the database
async def add_user(user: dict) -> bool:
    new_user = User().dict()
    for key in user.keys():
        new_user[key] = user[key]
    user = await user_collection.insert_one(new_user)
    await user_collection.find_one({"_id": ObjectId(user.inserted_id)})
    return True


# Retrieve a student with a matching ID
async def retrieve_user_by_steam_id(id: int) -> dict:
    user = await user_collection.find_one({"steam_id64": id})
    if user:
        return user


# Delete a student from the database
async def delete_user_by_id(id: int):
    user = await user_collection.find_one({"steam_id64": id})
    if user:
        await user_collection.delete_one({"steam_id64": id})
        return True

async def update_user_by_steam_id(id: int) -> dict:
    user = await user_collection.find_one({'steam_id64': id})
    if user:
        new_user = dict(user)
        del new_user['_id']
        count, stats = await update_last20(id=id)
        analyzed_matches = new_user['analyzed_matches'] + count
        for key in stats.keys():
            if type(new_user[key]) == int:
                new_user[key] = round((new_user[key] + stats[key]) / analyzed_matches, 2)
            else:
                new_user[key] = (new_user[key] + stats[key]) / analyzed_matches
        await user_collection.update_one({'_id': user['_id']},{"$set": dict(new_user)})
    if new_user is None:
        return False
    return await user_collection.find_one({'steam_id64': id})

async def update_user_line() -> bool:
    async for user in user_line_collection.find():
        url = f'https://open.faceit.com/data/v4/players?game=csgo&game_player_id={user["steam_id"]}'
        request = requests.get(url, headers=headers)
        json_resp = json.loads(request.text)
        if await user_collection.find_one({'steam_id64': user['steam_id']}) is None:
            await add_user({
                'steam_id64': user['steam_id'],
                'nickname': json_resp['nickname']
            })
        await update_user_by_steam_id(id=user['steam_id'])
        await user_line_collection.delete({'steam_id': user['steam_id']})
    return True