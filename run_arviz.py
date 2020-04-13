import arviz as az
import json
import numpy as np
import pandas as pd

with open("8school_results.json") as f:
    res = json.load(f)

res = np.array(res)
print(res.shape)
res = {'X' : np.swapaxes(res, 0, 1)}
res_warmup = {"X" : res["X"][:, :-100, :]}
res = {"X" : res["X"][:, -100:, :]}
print(res.shape)
print(res_warmup.shape)
idata = az.from_dict(res)
print(idata)

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

print(az.summary(idata))

with open("8school_results_monitor.json") as f:
    res_monitor = json.load(f)

print(res_monitor)
