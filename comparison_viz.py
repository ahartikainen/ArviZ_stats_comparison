import os

import holoviews as hv
import numpy as np
import pandas as pd
from bokeh.models import HoverTool

hv.extension("bokeh")

if os.environ.get("USEGIT") == "true":
    env_name = "git"
else:
    env_name = "pypi-cran"

df_r = pd.read_csv(f"reference_posterior_{env_name}.csv", index_col=0).reset_index(drop=True)
df_py = (
    pd.read_csv(f"reference_arviz_{env_name}.csv", index_col=0)
    .reset_index(drop=True)
    .drop(columns="index")
)

df_r_unstack = (
    df_r.unstack()
    .reset_index()
    .rename(columns={"level_0": "diagnostic", "level_1": "value_index", 0: "r_values"})
)
df_py_unstack = (
    df_py.unstack()
    .reset_index()
    .rename(columns={"level_0": "diagnostic", "level_1": "value_index", 0: "py_values"})
)

comparison = df_r_unstack.merge(df_py_unstack)
comparison["diff"] = comparison["r_values"] - comparison["py_values"]
comparison["quality"] = np.ceil(np.log10(abs(comparison["diff"])))
quality_map = dict(comparison.groupby("diagnostic")["quality"].max().astype(int))
quality_map = {key: f"1e{value}" for key, value in quality_map.items()}
comparison["quality"] = comparison["diagnostic"].apply(quality_map.get)
comparison["group"] = comparison["diagnostic"].apply(
    lambda x: "rhat"
    if "rhat" in x
    else "ess"
    if "ess" in x
    else "mcse"
    if "mcse" in x
    else "WHAT"
)
for key, func in [
    ("diff_max", np.max),
    ("diff_min", np.min),
    ("diff_mean", np.mean),
    ("diff_median", np.median),
]:
    for group, items in comparison.groupby("diagnostic")["diff"]:
        comparison.loc[items.index, key] = "{:.2e}".format(func(items.values))

hover_tool_rhat = HoverTool(
    tooltips=[
        ("function", "@diagnostic"),
        ("max", "@diff_max"),
        ("min", "@diff_min_rhat"),
    ]
)

hover_tool_ess = HoverTool(
    tooltips=[
        ("function", "@diagnostic"),
        ("max", "@diff_max"),
        ("min", "@diff_min_ess"),
    ]
)

hover_tool = HoverTool(
    tooltips=[
        ("function", "@diagnostic"),
        ("max", "@diff_max"),
        ("min", "@diff_min"),
    ]
)

TOOLS_rhat = ["save", "pan", "reset", hover_tool_rhat, "ybox_zoom", "ywheel_zoom"]
TOOLS_ess = ["save", "pan", "reset", hover_tool_ess, "ybox_zoom", "ywheel_zoom"]
TOOLS_mcse = ["save", "pan", "reset", hover_tool, "ybox_zoom", "ywheel_zoom"]

title = "rhat accuracy"
boxwhisker = hv.BoxWhisker(
    comparison[comparison.group == "rhat"].rename(
        columns={"diff_min": "diff_min_rhat", "diff": "diff_rhat"}
    ),
    ["diagnostic", "diff_min_rhat", "diff_max"],
    ["diff_rhat"],
    label=title,
)
boxwhisker.opts(
    show_legend=False,
    width=400,
    show_grid=True,
    tools=TOOLS_rhat,
    default_tools=[],
    xlabel="",
)

title = "ess"
boxwhisker2 = hv.BoxWhisker(
    comparison[comparison.group == "ess"].rename(
        columns={"diff_min": "diff_min_ess", "diff": "diff_ess"}
    ),
    ["diagnostic", "diff_min_ess", "diff_max"],
    "diff_ess",
    label=title,
)
boxwhisker2.opts(
    show_legend=False,
    width=800,
    show_grid=True,
    tools=TOOLS_ess,
    default_tools=[],
    box_fill_color="orange",
    xlabel="",
)

title = "mcse"
boxwhisker3 = hv.BoxWhisker(
    comparison[comparison.group == "mcse"].rename(columns={"diff": "diff_mcse"}),
    ["diagnostic", "diff_min", "diff_max"],
    "diff_mcse",
    label=title,
)
boxwhisker3.opts(
    show_legend=False,
    width=600,
    show_grid=True,
    tools=TOOLS_mcse,
    default_tools=[],
    box_fill_color="yellow",
    xlabel="",
)

layout = hv.Layout((boxwhisker, boxwhisker2, boxwhisker3)).cols(1)
renderer = hv.renderer("bokeh")
renderer.save(layout, f"posterior_arviz_convergence_{env_name}")
