from models import *

def parse_team(team_data) -> Team:
    return Team(
        code=team_data['code'],
        name=team_data['name'],
        slug=team_data['slug'],
        result=Result(
            gameWins=team_data.get('result', {}).get('gameWins', 0),
            outcome=team_data.get('result', {}).get('outcome', '')
        ) if 'result' in team_data else None,
        record=Record(
            losses=team_data.get('record', {}).get('losses', 0),
            wins=team_data.get('record', {}).get('wins', 0)
        ) if 'record' in team_data else None
    )

def parse_match(match_data) -> Match:
    return Match(
        id=match_data['id'],
        teams=[parse_team(team) for team in match_data.get('teams', [])],
        strategy=Strategy(
            count=match_data.get('strategy', {}).get('count', 0),
            type=match_data.get('strategy', {}).get('type', '')
        ) if 'strategy' in match_data else None
    )

def parse_tournament(tournament_data) -> Tournament:
    return Tournament(
        id=tournament_data['id'],
        slug=tournament_data['slug'],
        startDate=tournament_data['startDate'],
        endDate=tournament_data['endDate']
    )

def parse_league(league_data) -> League:
    return League(
        id=league_data.get('id', ''),
        slug=league_data.get('slug', ''),
        name=league_data.get('name', ''),
        region=league_data.get('region', '')
    )

def parse_event(event_data) -> Event:
    return Event(
        id=event_data['id'],
        type=event_data['type'],
        startTime=event_data['startTime'],
        blockName=event_data['blockName'],
        state=event_data['state'],
        match=parse_match(event_data['match']) if 'match' in event_data else None,
        league=parse_league(event_data['league']) if 'league' in event_data else None
    )