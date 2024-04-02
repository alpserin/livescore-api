import requests
import os
from dotenv import load_dotenv
from collections import defaultdict

load_dotenv('.env')
KEY = os.getenv('KEY')
SECRET = os.getenv('SECRET')
BASE_DOMAIN = os.getenv('BASE_DOMAIN')

def get_country_name(country_id):
    try:
        path = f"{BASE_DOMAIN}" + f"/countries/list.json?&key={KEY}&secret={SECRET}"
        response = requests.get(path)
        data = response.json()
        for i in range(len(data['data']['country'])):
            if (int(data['data']['country'][i]['id']) == country_id):
                return data['data']['country'][i]['name']
    except Exception:
        print(f"Couldn't get country data. Check your api key or the url.")
        raise Exception

def get_competition_data(competition_id):
    try:
        path = f"{BASE_DOMAIN}" + f"/competitions/table.json?competition_id={competition_id}&key={KEY}&secret={SECRET}"
        response = requests.get(path)
        data = response.json()
        return data['data']['stages'][0]['groups']
    except Exception:
        print(f"Couldn't get competititon data. Check your api key or the url.")
        raise Exception

def calculate_win_percentage(team_data):
    try:
        won = team_data['won']
        drawn = team_data['drawn']
        lost = team_data['lost']
        total_matches = won + drawn + lost
        perc = (won / total_matches) * 100
        return perc
    except:
        print("Couldn't calculate win percentage.")


def main():

    try:
        competition_id = 244 # ID for UEFA Champions League
        competition_data = get_competition_data(competition_id)

        country_team_count = defaultdict(int)
        country_win_perc = defaultdict(float)
        country_match_count = defaultdict(int)
        country_teams = defaultdict(list)

        for group in competition_data:
            for team_data in group['standings']:
                team = team_data['team']
                country_id = team['country_id']
                country_name = get_country_name(country_id)
                country_team_count[country_name] += 1
                perc = calculate_win_percentage(team_data)
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
    except Exception as error:
        print(f"{error}")

if __name__ == "__main__":
    main()
