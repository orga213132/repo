from dataclasses import Field
from pydantic import BaseModel
from models.player import Player
from typing import List

class Match(BaseModel):
    map: str
    team1: str
    team2: str
    winner: str
    players1: List[Player]
    players2: List[Player]
    final_score: str
    
