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
print(res["X"].shape)
print(res_warmup["X"].shape)
idata = az.from_dict(res)
print(idata)

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

print(az.summary(idata))

with open("8school_results_monitor.json") as f:
    res_monitor = json.load(f)

print(res_monitor)

reference = pd.read_csv("./reference_values.csv", index_col=0).sort_index(axis=1).sort_index(axis=0)

# test arviz functions
funcs = {
    "rhat_rank": lambda x: rhat(x, method="rank"),
    "rhat_raw": lambda x: rhat(x, method="identity"),
    "ess_bulk": lambda x: ess(x, method="bulk"),
    "ess_tail": lambda x: ess(x, method="tail"),
    "ess_mean": lambda x: ess(x, method="mean"),
    "ess_sd": lambda x: ess(x, method="sd"),
    "ess_raw": lambda x: ess(x, method="identity"),
    "ess_quantile01": lambda x: ess(x, method="quantile", prob=0.01),
    "ess_quantile10": lambda x: ess(x, method="quantile", prob=0.1),
    "ess_quantile30": lambda x: ess(x, method="quantile", prob=0.3),
    "mcse_mean": lambda x: mcse(x, method="mean"),
    "mcse_sd": lambda x: mcse(x, method="sd"),
    "mcse_quantile01": lambda x: mcse(x, method="quantile", prob=0.01),
    "mcse_quantile10": lambda x: mcse(x, method="quantile", prob=0.1),
    "mcse_quantile30": lambda x: mcse(x, method="quantile", prob=0.3),
}
results = {}
for key, coord_dict, vals in az.plots.plot_utils.xarray_var_iter(idata.posterior, combined=True):
    if coord_dict:
        key = key + ".{}".format(list(coord_dict.values())[0] + 1)
    results[key] = {func_name: func(vals) for func_name, func in funcs.items()}
arviz_data = pd.DataFrame.from_dict(results).T.sort_index(axis=1).sort_index(axis=0)

# check column names
print("Column names are the same:", set(arviz_data.columns) == set(reference.columns))
# check parameter names
# assert set(arviz_data.index) == set(reference.index)
# check equality (rhat_rank has accuracy < 6e-5, atleast with this data, R vs Py)
# this is due to numerical accuracy in calculation leading to rankdata
# function, which scales minimal difference to larger scale
# test first with numpy
print(reference)
print(arviz_data)
print(reference-arviz_data)
print((reference-arviz_data).max(0))
print((reference-arviz_data).max(1))
print((reference-arviz_data).max().max())
# then test manually (more strict)
#assert (abs(reference["rhat_rank"] - arviz_data["rhat_rank"]) < 6e-5).all(None)
#assert abs(np.median(reference["rhat_rank"] - arviz_data["rhat_rank"]) < 1e-14).all(None)
#not_rhat = [col for col in reference.columns if col != "rhat_rank"]
#assert (abs((reference[not_rhat] - arviz_data[not_rhat])).values < 1e-8).all(None)
#assert abs(np.median(reference[not_rhat] - arviz_data[not_rhat]) < 1e-14).all(None)
