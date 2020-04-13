import arviz as az
import json
import numpy as np
import pandas as pd

with open("8school_results.json") as f:
    res = json.load(f)

print(res)
res = {key : np.array(values) for key, values in res[0].items()}
idata = az.from_dict(df_dict)
print(idata)
print(az.summary(idata))

with open("8school_results_monitor.json") as f:
    res_monitor = json.load(f)

print(res_monitor)
