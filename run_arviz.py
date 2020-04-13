import arviz as az
import pandas as pd

df = pd.read_csv("8school_results.csv")

print(df)
df_dict = df.to_dict(orient="list")
print(df_dict)
idata = az.from_dict(df_dict)
print(idata)
print(az.summary(idata))
