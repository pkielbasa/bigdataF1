import matplotlib.pyplot as plt
from pyergast import pyergast
from pathlib import Path
import numpy as np

driversStandings = pyergast.driver_standings(2022)
standings = driversStandings.drop(columns=["constructorID", "constructor", "nationality",  "driverID", "positionText"])
position = standings['position'].value_counts().sort_index().to_frame()
points = standings['points'].values
names = standings['driver'].values
wins = standings['wins'].values
T3 = list(map(int, points))
T2 = list(map(int, wins))
print(standings)
X_axis = np.arange(len(names))
fig = plt.figure(figsize=(35, 4))
plt.bar(X_axis - 0.2, T2, 0.4, label = 'Wins')
plt.bar(X_axis + 0.2, T3, 0.4, label = 'Points',color='red')
plt.xticks(X_axis, names)
plt.xlabel("Driver")
plt.ylabel("Number of Points & Wins ")
plt.title("F1 2022 Driver Standings")
plt.savefig('standingPoints.png')
plt.legend()
plt.show()
filepath = Path('standingsPoints.csv')
filepath.parent.mkdir(parents=True, exist_ok=True)
standings.to_csv(filepath, index=False)
