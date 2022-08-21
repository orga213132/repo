import motor.motor_asyncio
from core.config import DATABASE_URL
MONGO_DETAILS = DATABASE_URL
from bson import ObjectId

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.scopegg

user_collection = database.get_collection('users_collection')
match_collection = database.get_collection('matches_collection')
analyzed_demo_collection = database.get_collection('analyzed_demos_collection')
user_line_collection = database.get_collection('users_line_collection')

def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "steam_id64": user['steam_id64'],
        "nickname": user["nickname"],
        'created_at': user['created_at'],
        'analyzed_matches': user['analyzed_matches'],
        'kd': user['kd'],
        'hltv_rating': user['hltv_rating'],
        'kast': user['kast'],
        'winrate': user['winrate'],
        'adr': user['adr'],
        'akr': user['akr'],
    }

def match_helper(match) -> dict:
    return {
        'id': str(match['_id']),
        'players': match['players'],
        'final_score': match['final_score'],
        'map': match['map'],
    }