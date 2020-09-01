import json
import os

import numpy as np
import pandas as pd

import arviz as az

if os.environ.get("USEGIT") == "true":
    env_name = "git"
else:
    env_name = "pypi-cran"

with open(f"8school_results_{env_name}.json") as f:
    res = json.load(f)

res = np.array(res)
print(res.shape)
res = {"X": np.swapaxes(res, 0, 1)}
res_warmup = {"X": res["X"][:, :-100, :]}
res = {"X": res["X"][:, -100:, :]}
print(res["X"].shape)
print(res_warmup["X"].shape)
idata = az.from_dict(res)
print(idata)

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)

print(az.summary(idata))

with open(f"posterior_summary_{env_name}.json") as f:
    res_posterior_summary = json.load(f)

res_posterior_summary = pd.DataFrame.from_records(
    res_posterior_summary, index="variable"
)
res_posterior_summary.index.name = None
print(res_posterior_summary)

reference = (
    pd.read_csv(
        f"./reference_posterior_{env_name}.csv", index_col=0, float_precision="high"
    )
    .reset_index()
    .astype(float)
)

# test arviz functions
funcs = {
    "rhat_rank": lambda x: az.rhat(x, method="rank"),
    "rhat_raw": lambda x: az.rhat(x, method="identity"),
    "ess_bulk": lambda x: az.ess(x, method="bulk"),
    "ess_tail": lambda x: az.ess(x, method="tail"),
    "ess_mean": lambda x: az.ess(x, method="mean"),
    "ess_sd": lambda x: az.ess(x, method="sd"),
    "ess_median": lambda x: az.ess(x, method="median"),
    "ess_raw": lambda x: az.ess(x, method="identity"),
    "ess_quantile01": lambda x: az.ess(x, method="quantile", prob=0.01),
    "ess_quantile10": lambda x: az.ess(x, method="quantile", prob=0.1),
    "ess_quantile30": lambda x: az.ess(x, method="quantile", prob=0.3),
    "mcse_mean": lambda x: az.mcse(x, method="mean"),
    "mcse_sd": lambda x: az.mcse(x, method="sd"),
    "mcse_median": lambda x: az.mcse(x, method="quantile", prob=0.5),
    "mcse_quantile01": lambda x: az.mcse(x, method="quantile", prob=0.01),
    "mcse_quantile10": lambda x: az.mcse(x, method="quantile", prob=0.1),
    "mcse_quantile30": lambda x: az.mcse(x, method="quantile", prob=0.3),
}
results = {}
for key, coord_dict, vals in az.plots.plot_utils.xarray_var_iter(
    idata.posterior, combined=True
):
    if coord_dict:
        key = "{}".format(list(coord_dict.values())[0] + 1)
    results[key] = {func_name: func(vals) for func_name, func in funcs.items()}
arviz_data = pd.DataFrame.from_dict(results).T.reset_index().astype(float)

# check column names
print("Column names are the same:", set(arviz_data.columns) == set(reference.columns))
# check parameter names
# assert set(arviz_data.index) == set(reference.index)
# check equality (rhat_rank has accuracy < 6e-5, atleast with this data, R vs Py)
# this is due to numerical accuracy in calculation leading to rankdata
# function, which scales minimal difference to larger scale
# test first with numpy
print("POSTERIOR")
print(reference)
print("\n\nARVIZ")
print(arviz_data)
print("\n\nPOSTERIOR - ARVIZ")
print(reference - arviz_data)
print("\n\nMAX ABS DIFF")
print((reference - arviz_data).abs().max(0))
print((reference - arviz_data).abs().max(1))
print("\n\nMAX ABS")
print((reference - arviz_data).abs().max().max())

arviz_data.to_csv(f"./reference_arviz_{env_name}.csv")

# then test manually (more strict)
# assert (abs(reference["rhat_rank"] - arviz_data["rhat_rank"]) < 6e-5).all(None)
# assert abs(np.median(reference["rhat_rank"] - arviz_data["rhat_rank"]) < 1e-14).all(None)
# not_rhat = [col for col in reference.columns if col != "rhat_rank"]
# assert (abs((reference[not_rhat] - arviz_data[not_rhat])).values < 1e-8).all(None)
# assert abs(np.median(reference[not_rhat] - arviz_data[not_rhat]) < 1e-14).all(None)
