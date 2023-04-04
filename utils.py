import pandas as pd 

data = pd.read_json('workout-data.json').to_csv('workout-data.csv',index=False)

    