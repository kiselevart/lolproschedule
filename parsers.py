from models import *

def parse_result(result_data) -> Result:
    if result_data is None:
        return Result(gameWins=0, outcome='')

    return Result(
        gameWins=result_data.get('gameWins', 0),
        outcome=result_data.get('outcome', '')
    )

def parse_record(record_data) -> Record:
    if record_data is None:
        return Record(losses=0, wins=0)

    return Record(
        losses=record_data.get('losses', 0),
        wins=record_data.get('wins', 0)
    )

def parse_team(team_data) -> Team:
    return Team(
        code=team_data.get('code'),
        name=team_data.get('name'),
        slug=team_data.get('slug'),
        result=parse_result(team_data.get('result', {})),
        record=parse_record(team_data.get('record', {}))
    )

def parse_strategy(strategy_data) -> Strategy:
    return Strategy(
        count=strategy_data.get('count', 0),
        type=strategy_data.get('type', '')
    )

def parse_match(match_data) -> Match:
    return Match(
        id=match_data.get('id'),
        teams=[parse_team(team) for team in match_data.get('teams', [])],
        strategy=parse_strategy(match_data.get('strategy', {}))
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
        id=event_data.get('id'),
        type=event_data.get('type'),
        startTime=event_data.get('startTime'),
        blockName=event_data.get('blockName'),
        state=event_data.get('state'),
        match=parse_match(event_data['match']) if 'match' in event_data else None,
        league=parse_league(event_data['league']) if 'league' in event_data else None
    )

def parse_events(events_data) -> List[Event]:
    return [parse_event(event_data) for event_data in events_data]


def parse_pages(pages_data) -> AppPages:
    return AppPages(
        older=pages_data.get('older', ''),
        newer=pages_data.get('newer', '')
    )

def parse_schedule(schedule_data) -> Schedule:
    return Schedule(
        updated=schedule_data.get('updated', 'Unknown'),
        pages=parse_pages(schedule_data.get('pages', {})),
        events=parse_events(schedule_data.get('events', []))
    )