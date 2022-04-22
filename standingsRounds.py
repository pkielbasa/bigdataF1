import fastf1 as ff1
import matplotlib.pyplot as plt
import pandas as pd
import requests
import seaborn as sns
from fastf1 import plotting
from pathlib import Path
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


def ergast_retrieve(api_endpoint: str):
    url = f'https://ergast.com/api/f1/{api_endpoint}.json'
    response = requests.get(url).json()

    return response['MRData']


rounds = 3

all_championship_standings = pd.DataFrame()

driver_team_mapping = {}

for i in range(1, rounds + 1):
    race = ergast_retrieve(f'2022/{i}/driverStandings')

    standings = race['StandingsTable']['StandingsLists'][0]['DriverStandings']

    current_round = {'round': i}

    for i in range(len(standings)):
        driver = standings[i]['Driver']['code']
        position = standings[i]['position']

        current_round[driver] = int(position)

        driver_team_mapping[driver] = standings[i]['Constructors'][0]['name']

    all_championship_standings = all_championship_standings.append(current_round, ignore_index=True)

all_championship_standings = all_championship_standings.set_index('round')
all_championship_standings_melted = pd.melt(all_championship_standings.reset_index(), ['round'])
sns.set(rc={'figure.figsize': (11.7, 8.27)})
all_championship_standings_melted['value'] = all_championship_standings_melted['value'].fillna(21.0)

print(all_championship_standings_melted['value'])
fig, ax = plt.subplots()

ax.set_title("2022 Championship Standings")


for driver in pd.unique(all_championship_standings_melted['variable']):
    sns.lineplot(
        x='round',
        y='value',
        data=all_championship_standings_melted.loc[all_championship_standings_melted['variable'] == driver],
        color=ff1.plotting.team_color(driver_team_mapping[driver])
    )

ax.invert_yaxis()

ax.set_xticks(range(1, rounds))
ax.set_yticks(range(1, 22))

ax.set_xlabel("Round")
ax.set_ylabel("Championship position")

ax.grid(False)

for line, name in zip(ax.lines, all_championship_standings.columns.tolist()):
    y = line.get_ydata()[-1]
    x = line.get_xdata()[-1]

    text = ax.annotate(
        name,
        xy=(x + 0.1, y),
        xytext=(0, 0),
        color=line.get_color(),
        xycoords=(
            ax.get_xaxis_transform(),
            ax.get_yaxis_transform()
        ),
        textcoords="offset points"
    )

plt.savefig('screens/championship_standings.png')
plt.show()
filepath = Path('csv/championship_standings.csv')
filepath.parent.mkdir(parents=True, exist_ok=True)
all_championship_standings_melted.to_csv(filepath, index=False)