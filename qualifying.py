import pandas as pd
import requests

import fastf1 as ff1
from fastf1 import plotting

import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path


def ergast_retrieve(api_endpoint: str):
    url = f'https://ergast.com/api/f1/{api_endpoint}.json'
    response = requests.get(url).json()

    return response['MRData']


all_quali_results = pd.DataFrame()

team_drivers = {}

current_round = 1

while True:
    race = ergast_retrieve(f'2022/{current_round}/qualifying')

    if not race['RaceTable']['Races']:
        break

    results = race['RaceTable']['Races'][0]['QualifyingResults']

    quali_results = {'round': current_round}

    for j in range(len(results)):
        driver = results[j]['Driver']['code']
        position = int(results[j]['position'])
        team = results[j]['Constructor']['name']



        if not team in team_drivers:
            team_drivers[team] = [driver]
        else:
            if not driver in team_drivers[team]:
                team_drivers[team].append(driver)

        quali_results[driver] = position

    all_quali_results = all_quali_results.append(quali_results, ignore_index=True)

    current_round += 1

all_quali_battle_results = []
team_colors_palette = []

for team in team_drivers:
    drivers = team_drivers[team]

    quali_results = all_quali_results[drivers]

    fastest_driver_per_round = quali_results.dropna().idxmin(axis=1)

    quali_battle_result = fastest_driver_per_round.value_counts().reset_index()

    for _, driver in quali_battle_result.iterrows():
        all_quali_battle_results.append({
            'driver': driver['index'],
            'team': team,
            'quali_score': driver[0]
        })

    team_colors_palette.append(ff1.plotting.team_color(team))
    team_colors_palette = ['#D3D3D3' if v is None else v for v in team_colors_palette]

all_quali_battle_results = pd.DataFrame.from_dict(all_quali_battle_results)
print(all_quali_battle_results)
# Increase the size of the plot
sns.set(rc={'figure.figsize':(11.7,8.27)})

custom_palette = sns.set_palette(sns.color_palette(team_colors_palette))

fig, ax = plt.subplots()

ax.set_title(f"2022 Teammate Qualifying Battle")

g = sns.barplot(
    x='driver',
    y='quali_score',
    hue='team',
    data=all_quali_battle_results,
    dodge=False,
    palette=custom_palette,
)

plt.yticks(range(max(all_quali_battle_results['quali_score']) + 1))

plt.legend([],[], frameon=False)

g.set(xlabel=None)
g.set(ylabel=None)

plt.savefig('screens/qualifying_battles.png')

plt.show()
print(all_quali_battle_results)
filepath = Path('csv/qualifying.csv')
filepath.parent.mkdir(parents=True, exist_ok=True)
all_quali_battle_results.to_csv(filepath, index=False)