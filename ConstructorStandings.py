import matplotlib.pyplot as plt
from pyergast import pyergast
from pathlib import Path
import numpy as np
constructorStandings = pyergast.constructor_standings(2022)

standings = constructorStandings.drop(columns=["constructorID", "nationality",  "positionText"])
position = standings['position'].value_counts().sort_index().to_frame()
points = standings['points'].values
names = standings['name'].values
wins = standings['wins'].values
T3 = list(map(int, points))
T2 = list(map(int, wins))
print(standings)

X_axis = np.arange(len(names))
fig = plt.figure(figsize=(25, 4))
plt.bar(X_axis - 0.2, T2, 0.4, label = 'Wins')
plt.bar(X_axis + 0.2, T3, 0.4, label = 'Points')
plt.xticks(X_axis, names)
plt.xlabel("Driver")
plt.ylabel("Number of Points & Wins ")
plt.title("F1 2022 Constructor Standings")
plt.savefig('ConstructorStandings.png')
plt.legend()
plt.show()
filepath = Path('ConstructorStandings.csv')
filepath.parent.mkdir(parents=True, exist_ok=True)
standings.to_csv(filepath, index=False)
