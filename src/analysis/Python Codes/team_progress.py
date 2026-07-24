#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 19:35:05 2026

@author: amirreza
"""

from sqltopython import *

df = pd.read_csv('Q2_2.csv')
#%%
metrics = [
    "ORtg",
    "DRtg",
    "pace",
    "ast/G",
    "trb/G",
    "stl/G",
    "blk/G",
    "tov/G"
]

for metric in metrics:

    print("\n", "="*60)
    print(metric)

    summary = (
        df.groupby("Category")[metric]
          .agg(
              Count="count",
              Mean="mean",
              Median="median",
              Std="std",
              Min="min",
              Max="max"
          )
          .round(3)
    )

    print(summary)
#%%
for metric in metrics:

    print("\n")
    print("="*60)
    print(metric)

    for group in df["Category"].unique():

        data = df[df["Category"]==group][metric]

        W,p = shapiro(data)

        print(f"{group:20s} W={W:.4f} p={p:.4f}")
#%%

for metric in metrics:

    groups = [
        g[metric].dropna().values
        for _,g in df.groupby("Category")
    ]

    stat,p = levene(*groups)

    print(metric)
    print("Levene =",round(stat,4))
    print("p =",round(p,6))
    print()
#%%

for metric in metrics:

    groups = [
        g[metric].dropna().values
        for _,g in df.groupby("Category")
    ]

    F,p = f_oneway(*groups)

    print(metric)
    print("F =",round(F,4))
    print("p =",p)
    print()
#%%

for metric in metrics:

    groups = [
        g[metric].dropna().values
        for _,g in df.groupby("Category")
    ]

    grand_mean = df[metric].mean()

    ss_between = sum(
        len(g)*(g.mean()-grand_mean)**2
        for g in groups
    )

    ss_total = ((df[metric]-grand_mean)**2).sum()

    eta2 = ss_between/ss_total

    print(metric)
    print("Eta squared =",round(eta2,4))
    print()
#%%

for metric in metrics:

    print("\n")
    print("="*60)
    print(metric)

    tukey = pairwise_tukeyhsd(
        endog=df[metric],
        groups=df["Category"],
        alpha=0.05
    )

    print(tukey)
#%%

pio.renderers.default = "browser"

color_map = {
    "High Progress": "#1F4E79",
    "No Change": "#A6A6A6",
    "Regression": "#D4AF37"
}

fig = px.box(
    df,
    x="Category",
    y="ORtg",
    color="Category",
    points="all",
    color_discrete_map=color_map
)

fig.update_traces(
    marker=dict(size=6, opacity=0.65)
)

fig.update_layout(
    template="plotly_white",
    width=900,
    height=600,
    title=dict(
        text="Comparison of Offensive Rating Across Improvement Categories",
        x=0.5
    ),
    xaxis_title="Team Category",
    yaxis_title="Offensive Rating (ORtg)",
    font=dict(size=14),
    showlegend=False
)

fig.show()
#%%
fig = px.box(
    df,
    x="Category",
    y="DRtg",
    color="Category",
    points="all",
    color_discrete_map=color_map
)

fig.update_traces(
    marker=dict(size=6, opacity=0.65)
)

fig.update_layout(
    template="plotly_white",
    width=900,
    height=600,
    title=dict(
        text="Comparison of Defensive Rating Across Improvement Categories",
        x=0.5
    ),
    xaxis_title="Team Category",
    yaxis_title="Defensive Rating (DRtg)",
    font=dict(size=14),
    showlegend=False
)

fig.show()