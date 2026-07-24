#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 20:04:44 2026

@author: amirreza
"""

from sqltopython import *

df = pd.read_csv('Q3_1.csv')



team_best = (
    df.sort_values("Rank")
      .groupby(["Team Name","Position"], as_index=False)
      .first())

heat = team_best.pivot(
    index="Team Name",
    columns="Position",
    values="Rank")

fig = px.imshow(
    heat,
    color_continuous_scale="RdYlGn_r",
    aspect="auto",
    text_auto=True)

fig.update_layout(
    template="plotly_white",
    width=900,
    height=900,
    title=dict(
        text="League Rank of Each Team's Best Player by Position",
        x=0.5
    ),
    coloraxis_colorbar=dict(title="League Rank"))

fig.show()
fig = px.box(
    df,
    x="Position",
    y="Rank",
    color="Position",
    color_discrete_sequence=[
        "#1F4E79",
        "#D4AF37",
        "#5A5A5A",
        "#4C78A8",
        "#E15759"
    ],
    points="all")

fig.update_layout(
    template="plotly_white",
    width=900,
    height=600,
    title=dict(
        text="Distribution of League Rankings by Position",
        x=0.5
    ),
    xaxis_title="Position",
    yaxis_title="League Rank",
    showlegend=False)

fig.update_yaxes(autorange="reversed")

fig.show()