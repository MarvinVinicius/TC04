import numpy as np, pandas as pd
df = pd.read_parquet("data/production/holdout.parquet").sample(500, random_state=1).reset_index(drop=True)
df.loc[0, "age"] = 15
df.loc[1, "MonthlyIncome"] = np.nan
df.loc[2, "DebtRatio"] = -1.0
df = pd.concat([df, df.iloc[3:8]], ignore_index=True)   # duplicadas
df = df.drop(columns=["NumberOfDependents"])             # coluna faltando
df.to_parquet("data/incoming/bad_batch.parquet")
pd.read_parquet("data/production/holdout.parquet").sample(500, random_state=2)\
  .to_parquet("data/incoming/good_batch.parquet")
