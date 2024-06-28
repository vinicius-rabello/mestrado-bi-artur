import pandas as pd

df = pd.read_excel('database/tables/possiveis_matches.xlsx')
print(df.groupby(['IdCenso']).sum())