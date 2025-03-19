import pandas as pd

df = pd.read_excel('./database/tables/censo38_corrigido.xlsx')
df['id'] = df.index
df.to_excel('./database/tables/censo38_corrigido.xlsx', index=False)