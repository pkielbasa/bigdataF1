import pandas as pd
import requests
import json
import matplotlib.pyplot as plt
from pathlib import Path

url = 'http://ergast.com/api/f1/status/.json'
statusResponse = requests.get(url)
statusRace = json.loads(statusResponse.text)
races = pd.DataFrame.from_dict(statusRace["MRData"]["StatusTable"])
df = pd.json_normalize(races["Status"])
df = df.drop(columns=["statusId"])
count = df['count'].values
status = df['status'].values

fig = plt.figure(figsize=(30,10))
print(df)
plt.pie(count, labels = status,autopct='%1.2f%%')
plt.savefig('screens/status.png')
plt.show()
filepath = Path('csv/status.csv')
filepath.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(filepath, index=False)

