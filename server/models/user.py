from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    steam_id64: int = Field(...)
    nickname: str = Field(...)
    created_at: datetime = datetime.utcnow()
    analyzed_matches: int = 0
    kills: int = 0
    deaths: int = 0
    kdr: float = 0.0
    assists: int = 0
    tradeKills: int = 0
    teamKills: int = 0
    suicides: int = 0
    flashAssists: int = 0
    totalDamageGiven: int = 0
    totalDamageTaken: int = 0
    totalTeamDamageGiven: int = 0
    adr: float = 0.0
    totalShots: int = 0
    shotsHit: int = 0
    accuracy: float = 0.0
    rating: float = 0.0
    kast: float = 0.0
    hs: int = 0
    hsPercent: float = 0.0
    firstKills: int = 0
    firstDeaths: int = 0
    utilityDamage: int = 0
    smokesThrown: int = 0
    flashesThrown: int = 0
    heThrown: int = 0
    fireThrown: int = 0
    enemiesFlashed: int = 0
    teammatesFlashed: int = 0
    blindTime: float = 0.0
    plants: int = 0
    defuses: int = 0

