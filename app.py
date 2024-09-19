from parsers import *

from flask import Flask, render_template
import requests
from typing import List, Optional

# Flask app initialization
app = Flask(__name__)

# General data
apiKey = '0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z'
baseUrl = 'https://esports-api.lolesports.com/persisted/gw/'
headers = {'x-api-key': apiKey}

def get_leagues() -> List[League]:
    leaguesUrl = 'getLeagues?hl=en-US'
    leaguesResponse = requests.get(baseUrl + leaguesUrl, headers=headers)
    
    if leaguesResponse.status_code != 200:
        print("getleagues error")
        return []

    raw_data = leaguesResponse.json()
    leagues_data = raw_data.get('data', {}).get('leagues', [])
    
    leagues = [parse_league(league) for league in leagues_data]
    
    return leagues

def get_tournaments(leagueId: str) -> List[Tournament]:
    tournamentsUrl = f'getTournamentsForLeague?hl=en-US&leagueId={leagueId}'
    tournamentsResponse = requests.get(baseUrl + tournamentsUrl, headers=headers)
    
    if tournamentsResponse.status_code != 200:
        print("gettournaments error")
        return []

    raw_data = tournamentsResponse.json()
    leagues_data = raw_data.get('data', {}).get('leagues', [{}])
    tournaments_data = leagues_data[0].get('tournaments', [])
    
    tournaments = [parse_tournament(tournament) for tournament in tournaments_data]
    
    return tournaments

def get_schedule() -> Schedule:
    scheduleUrl = 'getSchedule?hl=en-US'
    scheduleResponse = requests.get(baseUrl + scheduleUrl, headers=headers)

    if scheduleResponse.status_code != 200:
        print("getschedule error")
        return[]

    raw_data = scheduleResponse.json()
    schedule_data = raw_data.get('data', {}).get('schedule', [])

    schedule = parse_schedule(schedule_data)

    return schedule 

def get_upcoming_schedule(schedule) -> Schedule:
    print(schedule.events)
    for event in schedule.events:
        print("FORLOOP")
        print(event)

    

# REWRITE
# def get_live() -> List[Event]:
#     liveUrl = 'getLive?hl=en-US'
#     liveResponse = requests.get(baseUrl + liveUrl, headers=headers)
    
#     if liveResponse.status_code != 200:
#         print("getlive error")
#         return []

#     raw_data = liveResponse.json()
#     events_data = raw_data.get('data', {}).get('events', [])

#     events = [parse_event(event) for event in events_data]

#     return events


# Flask route to render leagues
@app.route('/')
def index():
    leagues = get_leagues()
    tournaments = get_tournaments(98767991299243165)
    schedule = get_schedule()
    return render_template('index.html', leagues=leagues, tournaments=tournaments, schedule=schedule)


if __name__ == '__main__':
    app.run(debug=True)
