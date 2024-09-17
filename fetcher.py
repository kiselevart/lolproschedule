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

# Function to get leagues data
def get_leagues() -> List[League]:
    apikey = '0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z'
    url = 'https://esports-api.lolesports.com/persisted/gw/getLeagues?hl=en-US'
    headers = {'x-api-key': apikey}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        raw_data = response.json()
        
        leagues: List[League] = [League(
            id=league['id'],
            slug=league['slug'],
            name=league['name'],
            region=league['region']
        ) for league in raw_data['data']['leagues']]
        
        return leagues
    else:
        return []

# Flask route to render leagues
@app.route('/')
def index():
    leagues = get_leagues()
    return render_template('index.html', leagues=leagues)

if __name__ == '__main__':
    app.run(debug=True)
