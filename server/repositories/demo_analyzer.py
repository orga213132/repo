from awpy import DemoParser
from awpy.analytics.stats import player_stats
import requests
import json
import gzip
import shutil
import os
from core.config import headers

 


async def analyze_match(match_id: str):
    url = f'https://open.faceit.com/data/v4/matches/{match_id}'
    request = requests.get(url, headers=headers)
    json_resp = json.loads(request.text)
    demo_url = json_resp['demo_url'][0]

    request = requests.get(demo_url, allow_redirects=True)
    name = demo_url.split('/')[-1]
    open(f'demos/{name}', 'wb').write(request.content)
    with gzip.open(f'demos/{name}', 'rb') as f_in:
        with open(f'demos/{name[:-3]}', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(f'demos/{name}')

    path = name[:-3]
    parser = DemoParser(
        demofile=f'demos/{path}',
        demo_id=path[:-4],
        parse_frames=False,
        parse_rate=128,
        json_indentation=False,
        outpath='demos/'
    )
    data = parser.parse()
    os.remove(f'demos/{path}')
    try:
        player_stats_json = player_stats(data['gameRounds'])
    except:
        return False

    url = f'https://open.faceit.com/data/v4/matches/{match_id}/stats'
    request = requests.get(url, headers=headers)
    json_resp = json.loads(request.text)
    match_stats = {
        'map': json_resp['rounds'][0]['round_stats']['Map'],
        'final_score': json_resp['rounds'][0]['round_stats']['Score'],
        'teams': {
            'team1': {
                'name': json_resp['rounds'][0]['teams'][0]['team_stats']['Team'],
                'is_win': json_resp['rounds'][0]['teams'][0]['team_stats']['Team Win']
            },
            'team2': {
                'name': json_resp['rounds'][0]['teams'][1]['team_stats']['Team'],
                'is_win': json_resp['rounds'][0]['teams'][1]['team_stats']['Team Win']
            }
        }

    }
    return player_stats_json, match_stats