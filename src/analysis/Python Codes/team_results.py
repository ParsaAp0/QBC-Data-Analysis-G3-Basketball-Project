#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 18:10:27 2026

@author: amirreza
"""

from sqltopython import *

df = pd.read_csv('Q1.csv')
#%%
metrics = [
    "ORtg",
    "DRtg",
    "pace",
    "ast/G",
    "trb/G",
    "stl/G",
    "tov/G"
]

summary = (
    df
    .groupby("rating")[metrics]
    .agg(["count", "mean", "median", "std"])
    .round(3)
)

print(summary)
#%%
results = []

for metric in metrics:

    top = df[df["rating"]=="Top 5"][metric]
    bottom = df[df["rating"]=="Down 15"][metric]

    # normality
    p1 = shapiro(top)[1]
    p2 = shapiro(bottom)[1]

    normal = (p1 > .05) and (p2 > .05)

    if normal:

        lev_p = levene(top,bottom)[1]

        equal = lev_p > .05

        stat,p = ttest_ind(
            top,
            bottom,
            equal_var=equal
        )

        pooled = np.sqrt(
            (
                ((len(top)-1)*top.var())+
                ((len(bottom)-1)*bottom.var())
            )/
            (len(top)+len(bottom)-2)
        )

        effect = (
            top.mean()-bottom.mean()
        )/pooled

        test = "t-test"

    else:

        stat,p = mannwhitneyu(
            top,
            bottom
        )

        n1=len(top)
        n2=len(bottom)

        z=(stat-n1*n2/2)/np.sqrt(
            n1*n2*(n1+n2+1)/12
        )

        effect=abs(z)/np.sqrt(n1+n2)

        test="Mann-Whitney"

    results.append([
        metric,
        test,
        round(p,5),
        round(effect,3)
    ])

results = pd.DataFrame(
    results,
    columns=[
        "Metric",
        "Test",
        "p-value",
        "Effect Size"
    ]
)

print(results)
#%%
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

pio.renderers.default = "browser"

metrics = [
    "ORtg",
    "DRtg",
    "pace",
    "ast/G",
    "trb/G",
    "stl/G",
    "tov/G"]

scaled = df.copy()

for col in metrics:
    scaled[col] = (scaled[col] - scaled[col].mean()) / scaled[col].std()


scaled["DRtg"] *= -1
scaled["tov/G"] *= -1

top5 = (
    scaled[scaled["rating"] == "Top 5"][metrics]
    .mean()
)

down15 = (
    scaled[scaled["rating"] == "Down 15"][metrics]
    .mean()
)

categories = metrics + [metrics[0]]

top_values = top5.tolist() + [top5.iloc[0]]
down_values = down15.tolist() + [down15.iloc[0]]


fig = go.Figure()

fig.add_trace(
    go.Scatterpolar(
        r=top_values,
        theta=categories,
        fill="toself",
        name="Top 5",
        line=dict(color="#1F4E79", width=3),
        fillcolor="rgba(31,78,121,0.25)"))

fig.add_trace(
    go.Scatterpolar(
        r=down_values,
        theta=categories,
        fill="toself",
        name="Bottom 15",
        line=dict(color="#D4AF37", width=3),
        fillcolor="rgba(212,175,55,0.25)"())

fig.update_layout(
    template="plotly_white",
    width=850,
    height=700,
    title=dict(
        text="Comparison of Team Performance Indicators",
        x=0.5
    ),
    polar=dict(
        radialaxis=dict(
            visible=True,
            showline=True,
            gridcolor="lightgray")),
    legend=dict(
        orientation="h",
        y=1.08,
        x=0.35))

fig.show()