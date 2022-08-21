from db.base import match_helper, match_collection, analyzed_demo_collection, user_line_collection
from bson import ObjectId
from models.matches import Match
import requests
from core.config import headers
import json
from .demo_analyzer import analyze_match

async def add_match(player_stats: list, match_stats: dict) -> bool:
    players1 = list()
    players2 = list()
    players_id = list()
    for player in player_stats.keys():
        players_id.append(player_stats[player]['steamID'])
        if player_stats[player]['playerName'] == match_stats['teams']['team1']['name']:
            players1.append(player_stats[player])
        else:
            players2.append(player_stats[player])

    match = {
        'map': match_stats['map'],
        'team1': match_stats['teams']['team1']['name'],
        'team2': match_stats['teams']['team2']['name'],
        'winner': '1' if match_stats['teams']['team1']['is_win'] == '1' else '2',
        'players1': players1,
        'players2': players2,
        'final_score': match_stats['final_score'] 
    }
    await match_collection.insert_one(match)
    for id in players_id:
        if await user_line_collection.find_one({'steam_id': id}) is None:
            await user_line_collection.insert_one({'steam_id': id})
    return True

async def delete_match(id: str) -> bool:
    match = await match_collection.find_one({"_id": ObjectId(id)})
    if match:
        await match_collection.delete_one({"_id": ObjectId(id)})
        return True
    return False

async def retrieve_by_steamid(id: int) -> list:
    matches = list()
    async for match in match_collection.find({'players': id}):
        matches.append(match_helper(match))
    return matches

async def update_last20(id: int):
    url = f"https://open.faceit.com/data/v4/players?game=csgo&game_player_id={id}"
    request = requests.get(url, headers=headers)
    js_resp = json.loads(request.text)
    faceit_id = js_resp['player_id']
    url = f'https://open.faceit.com/data/v4/players/{faceit_id}/history?game=csgo&offset=0&limit=20'
    request = requests.get(url, headers=headers)
    js_resp = json.loads(request.text)
    count = 0
    new_stats = {
        'kills': 0,
        'deaths': 0,
        'kdr': 0,
        'assists': 0,
        'tradeKills': 0,
        'teamKills': 0,
        'suicides': 0,
        'flashAssists': 0,
        'totalDamageGiven': 0,
        'totalDamageTaken': 0,
        'totalTeamDamageGiven': 0,
        'adr': 0,
        'totalShots': 0,
        'shotsHit': 0,
        'accuracy': 0,
        'rating': 0,
        'kast': 0,
        'hs': 0,
        'hsPercent': 0,
        'firstKills': 0,
        'firstDeaths': 0,
        'utilityDamage': 0,
        'smokesThrown': 0,
        'flashesThrown': 0,
        'heThrown': 0,
        'fireThrown': 0,
        'enemiesFlashed': 0,
        'teammatesFlashed': 0,
        'blindTime': 0,
        'plants': 0,
        'defuses': 0
    }
    for item in js_resp['items']:
        match_id = item['match_id']
        if await analyzed_demo_collection.find_one({'match_id': match_id}) is not None:
            continue
        count += 1
        try:
            players_stats, match_stats = await analyze_match(match_id=match_id)
        except:
            continue
        for player in players_stats.keys():
            if str(id) in player:
                for key in players_stats[player].keys():
                    if key == 'steamID':
                        if await user_line_collection.find_one({'steam_id': players_stats[player][key]}) is None and players_stats[player][key] != id and players_stats[player][key] != 0:
                            await user_line_collection.insert_one({'steam_id': players_stats[player][key]})
                    if key in new_stats.keys():
                        new_stats[key] += players_stats[player][key]
        await add_match(players_stats, match_stats)
        await analyzed_demo_collection.insert_one({'match_id': match_id})
    return count, new_stats
        
        