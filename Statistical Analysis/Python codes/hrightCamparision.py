#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 10:47:03 2026

@author: amirreza
"""

from sqltopython import*


height_query = """
SELECT
    PrimaryPosition AS Position,
    height
FROM
(
    SELECT
        TRIM(
            SUBSTRING_INDEX(
                REPLACE(
                    REPLACE(position,' and ',','),
                    '/',','
                ),
                ',',
                1
            )
        ) AS PrimaryPosition,
        height
    FROM Players
) t
WHERE PrimaryPosition IN
(
    'Point Guard',
    'Shooting Guard',
    'Small Forward',
    'Power Forward',
    'Center'
);

"""
#%%
height_df = run_query(height_query)
#%%
height_summary = (height_df.groupby("Position")["height"]
      .agg(
          Count="count",
          Mean="mean",
          Median="median",
          Std="std",
          Min="min",
          Max="max"
      )
      .round(2)
)

print(height_summary)
#%%

print("=" * 50)

for pos in sorted(height_df["Position"].unique()):

    data = height_df.loc[height_df["Position"] == pos, "height"]

    W, p = shapiro(data)

    print(f"{pos:18s}  W={W:.4f}   p={p:.4f}")
#%%
groups = [
    g["height"].values
    for _, g in df.groupby("Position")
]

stat, p = levene(*groups)

print(f"Levene Statistic = {stat:.4f}")
print(f"p-value = {p:.4f}")
#%%
groups = [
    g["height"].values
    for _, g in height_df.groupby("Position")
]

F, p = f_oneway(*groups)

print(f"F = {F:.4f}")
print(f"p = {p:.6f}")
#%%
grand_mean = height_df["height"].mean()

ss_between = sum(
    len(g) * (g.mean() - grand_mean) ** 2
    for _, g in height_df.groupby("Position")["height"])

ss_total = ((height_df["height"] - grand_mean) ** 2).sum()

eta_squared = ss_between / ss_total

print(f"Eta squared = {eta_squared:.4f}")
#%%
from statsmodels.stats.multicomp import pairwise_tukeyhsd

tukey = pairwise_tukeyhsd(
    endog=height_df["height"],
    groups=height_df["Position"],
    alpha=0.05
)

print(tukey)

#%%
import plotly.express as px
import plotly.io as pio

pio.renderers.default = "browser"

color_map = {
    "Point Guard": "#1F4E79",
    "Shooting Guard": "#4C78A8",
    "Small Forward": "#72B7B2",
    "Power Forward": "#F2C14E",
    "Center": "#D4AF37"
}

fig = px.box(
    height_df,
    x="Position",
    y="height",
    color="Position",
    points="outliers",
    color_discrete_map=color_map
)

fig.update_traces(
    line=dict(width=2)
)

fig.update_layout(
    template="plotly_white",
    width=950,
    height=600,
    title=dict(
        text="<b>Height Distribution Across Player Positions</b>",
        x=0.5
    ),
    xaxis_title="Position",
    yaxis_title="Height (cm)",
    showlegend=False,
    font=dict(size=14)
)

fig.show()
#%%
mean_height = (
    height_df.groupby("Position", as_index=False)["height"]
      .mean()
)

fig = px.bar(
    mean_height,
    x="Position",
    y="height",
    color="Position",
    text="height",
    color_discrete_map=color_map
)

fig.update_traces(
    texttemplate="%{text:.1f}",
    textposition="outside"
)

fig.update_layout(
    template="plotly_white",
    width=900,
    height=550,
    title=dict(
        text="<b>Average Height by Playing Position</b>",
        x=0.5
    ),
    xaxis_title="Position",
    yaxis_title="Average Height (cm)",
    showlegend=False
)

fig.show()


















