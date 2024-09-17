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

def get_tournament(leagueId: str) -> List[Tournament]:
    tournamentUrl = 'getTournamentsForLeague?hl=en-US?leagueId=' + leagueId
    tournamentsResponse = requests.get(baseUrl+tournamentUrl, headers=headers)
    print(tournamentsResponse.status_code)

# Flask route to render leagues
@app.route('/')
def index():
    leagues = get_leagues()
    return render_template('index.html', leagues=leagues)

    tournament = get_tournament()

if __name__ == '__main__':
    app.run(debug=True)
