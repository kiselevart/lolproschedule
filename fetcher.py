from flask import Flask, render_template
import requests
from dataclasses import dataclass
from typing import List

# Flask app initialization
app = Flask(__name__)

# League dataclass
@dataclass
class League:
    id: str
    slug: str
    name: str
    region: str

# Tournament dataclass
@dataclass
class Tournament:
    id: str
    slug: str
    startDate: str
    endDate: str

# General data
apiKey = '0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z'
baseUrl = 'https://esports-api.lolesports.com/persisted/gw/'
headers = {'x-api-key': apiKey}

# Function to get leagues data
def get_leagues() -> List[League]:
    leaguesUrl = 'getLeagues?hl=en-US'
    leaguesResponse = requests.get(baseUrl+leaguesUrl, headers=headers)

    if leaguesResponse.status_code == 200:
        raw_data = leaguesResponse.json()
        
        leagues: List[League] = [League(
            id=league['id'],
            slug=league['slug'],
            name=league['name'],
            region=league['region']
        ) for league in raw_data['data']['leagues']]
        
        return leagues
    else:
        return []

def get_tournaments(leagueId: str) -> List[Tournament]:
    tournamentsUrl = f'getTournamentsForLeague?hl=en-US&leagueId={leagueId}'
    tournamentsResponse = requests.get(baseUrl + tournamentsUrl, headers=headers)
    
    if tournamentsResponse.status_code == 200:
        raw_data = tournamentsResponse.json()
        leagues_data = raw_data.get('data', {}).get('leagues', [{}])
        tournaments_data = leagues_data[0].get('tournaments', [])
        
        tournaments: List[Tournament] = [Tournament(
            id=tournament['id'],
            slug=tournament['slug'],
            startDate=tournament['startDate'],
            endDate=tournament['endDate']
        ) for tournament in tournaments_data]
        
        return tournaments
    
    # Return an empty list if something goes wrong
    return []

# Flask route to render leagues
@app.route('/')
def index():
    leagues = get_leagues()
    tournament = get_tournaments(98767991299243165)
    print(tournament)
    return render_template('index.html', leagues=leagues)


if __name__ == '__main__':
    app.run(debug=True)
