import fetch from 'node-fetch'; // For Node.js environment
import moment from 'moment'; // Ensure correct import for moment

interface ESportsAPIReturnData {
    resultsHtml: string;
    fixturesHtml: string;
    resultsMonths: string;
    fixturesMonths: string;
}

interface ESportsLeagueSchedule {
    league: string;
    url: string | undefined;
    time: string;
    teamA: string;
    teamB: string;
}

interface EsportsAPILeagueResponseEntry {
    id: string;
    slug: string;
    name: string;
    region: string;
    image: string;
    priority: number;
}

interface EsportsAPILeagueResponse {
    data: {
        leagues: EsportsAPILeagueResponseEntry[];
    };
}

interface EsportsAPIEventListItem {
    startTime: string;

    match: {
        teams: {
            code: string;
            image: string;
        }[];
    };

    league: {
        id: string;
        slug: string;
        name: string;
    };
}

interface EsportsAPIEventListResponse {
    data: {
        esports: {
            events: EsportsAPIEventListItem[];
        };
    };
}

export default class ESportsAPI {
    private schedule: Map<string, Map<string, ESportsLeagueSchedule[]>> = new Map();

    constructor() {
        this.loadData();
    }

    private async loadData() {
        try {
            const leagueResponse = await fetch("https://esports-api.lolesports.com/persisted/gw/getLeagues?hl=en-US", {
                headers: { "x-api-key": "0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z" },
            });
            const leagueLists = await leagueResponse.json() as EsportsAPILeagueResponse;

            const leagueIds = leagueLists.data.leagues.map(l => l.id).join(",");

            const eventResponse = await fetch(`https://esports-api.lolesports.com/persisted/gw/getEventList?hl=en-US&leagueId=${leagueIds}`, {
                headers: { "x-api-key": "0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z" },
            });
            const events = await eventResponse.json() as EsportsAPIEventListResponse;

            const schedule: Map<string, Map<string, ESportsLeagueSchedule[]>> = new Map();
            events.data.esports.events.forEach(e => {
                const gameData: ESportsLeagueSchedule = {
                    league: e.league.slug,
                    url: e.league.slug,
                    time: e.startTime,
                    teamA: e.match.teams[0].code,
                    teamB: e.match.teams[1].code,
                };

                const formattedDate = moment(e.startTime).format("YYYY-MM-DD");

                if (!schedule.has(formattedDate)) {
                    schedule.set(formattedDate, new Map());
                }

                if (!schedule.get(formattedDate)!.has(e.league.name)) {
                    schedule.get(formattedDate)!.set(e.league.name, []);
                }

                schedule.get(formattedDate)!.get(e.league.name)!.push(gameData);
            });

            this.schedule = schedule;
            this.printSchedule();

        } catch (error) {
            console.error("Error loading data:", error);
        }
    }

    private printSchedule() {
        if (this.schedule.size === 0) {
            console.log("No schedule data available.");
            return;
        }

        for (const [date, leagues] of this.schedule) {
            console.log(`Date: ${date}`);
            for (const [league, games] of leagues) {
                console.log(`  League: ${league}`);
                games.forEach(game => {
                    const formattedTime = moment(game.time).format("YYYY-MM-DD HH:mm:ss");
                    console.log(`    ${game.teamA} vs ${game.teamB} at ${formattedTime}`);
                });
            }
        }
    }
}

// Create an instance of the ESportsAPI class to fetch and print data
new ESportsAPI();
