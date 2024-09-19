from dataclasses import dataclass
from typing import List, Optional

@dataclass
class League:
    id: str
    slug: str
    name: str
    region: str

@dataclass
class Tournament:
    id: str
    slug: str
    startDate: str
    endDate: str

@dataclass
class Strategy:
    count: int
    type: str

@dataclass
class Result:
    gameWins: int
    outcome: str

@dataclass
class Record:
    losses: int
    wins: int

@dataclass
class Team:
    code: str
    name: str
    slug: str
    result: Optional[Result] = None
    record: Optional[Record] = None

@dataclass
class Match:
    id: str
    teams: List[Team]
    strategy: Optional[Strategy] = None

@dataclass
class Event:
    id: str
    type: str
    startTime: str
    blockName: str
    state: str
    match: Optional[Match] = None
    league: Optional[League] = None

@dataclass
class AppPages:
    older: str
    newer: str

@dataclass
class Schedule:
    updated: str
    events: List[Event]
    pages: Optional[AppPages] = None
