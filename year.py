import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import requests

racesUrl = "http://ergast.com/api/f1.json"  # website api url
racesResponse = requests.get(racesUrl)
racesJson = json.loads(racesResponse.text)
races = pd.DataFrame.from_dict(racesJson["MRData"]["RaceTable"]["Races"])
totalRaces = int(racesJson["MRData"]["total"])
limitRaces = 100
offsetRaces = 0
races = pd.DataFrame()
while offsetRaces < totalRaces:
    dataset = racesUrl + "?limit=" + str(limitRaces) + "&offset=" + str(offsetRaces)
    offsetRaces = offsetRaces + 100
    subset = pd.DataFrame.from_dict(json.loads(requests.get(dataset).text)["MRData"]["RaceTable"]["Races"])
    frames = [races, subset]
    races = pd.concat(frames)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

races = races.reset_index()
races = races.drop(columns=["index", "url", "Circuit", "time", "Sprint", "Qualifying"])
year = races['season'].value_counts().sort_index().to_frame()
year.columns = ["number of races"]
f1_color = (255 / 255, 24 / 255, 1 / 255)
ax = year.plot.line(y='number of races', use_index=True, color=f1_color, figsize=(20, 10))
ax.set_xlabel("Year");
ax.set_ylabel("Number of Races");
ax.set_title("Number of Races over Time");
plt.savefig('years.png')
plt.show()
plt.close()
db = year.head(73)
print(year.head(73))

filepath = Path('year.csv')
filepath.parent.mkdir(parents=True, exist_ok=True)
db.to_csv(filepath)

