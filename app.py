import requests
import os
from dotenv import load_dotenv
from collections import defaultdict

load_dotenv('.env')
KEY = os.getenv('KEY')
SECRET = os.getenv('SECRET')

def get_competition_id():
    return 244

def get_country_name(id):
    path = f"https://livescore-api.com/api-client/countries/list.json?&key={KEY}&secret={SECRET}"
    x = requests.get(path)
    x = x.json()

    for i in range(len(x['data']['country'])):
        if (int(x['data']['country'][i]['id']) == id):
            return x['data']['country'][i]['name']

path = f"https://livescore-api.com/api-client/competitions/table.json?competition_id={get_competition_id()}&key={KEY}&secret={SECRET}"

r = requests.get(path)
r = r.json()
r = r['data']['stages'][0]['groups']


country_team_count = defaultdict(int)
country_win_perc = defaultdict(float)
country_match_count = defaultdict(int)
country_teams = defaultdict(list)

for group in r:
    for team_data in group['standings']:
        team = team_data['team']
        country_id = team['country_id']
        country_name = get_country_name(country_id)
        country_team_count[country_name] += 1
        
        # Get win percentage
        w = team_data['won']
        d = team_data['drawn']
        l = team_data['lost']
        total_matches = w + d + l
        perc = (w / total_matches) * 100
        country_win_perc[country_name] += perc
        country_match_count[country_name] += 1
        country_teams[country_name].append(team['name'])

# Average win percentage by country
for country, total_win_perc in country_win_perc.items():
    total_matches = country_match_count[country]
    avg_win_perc = total_win_perc / total_matches
    print(f"Country: {country}, Total Teams: {country_team_count[country]} ,Average Win Percentage: {avg_win_perc:.2f}", "%")
    for team in country_teams[country]:
        print(team)
