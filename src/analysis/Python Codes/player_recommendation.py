#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 20:33:26 2026

@author: amirreza
"""

from sqltopython import *

df = pd.read_csv('Q4.csv')
#%%
player = "Alex Sarr"

df_player = df[df["player_name"] == player].sort_values(
    "recommendation_score",
    ascending=False
)

fig = px.bar(
    df_player,
    x="destination_team",
    y="recommendation_score",
    color="acceptance_score",
    text="recommendation_score",
    title=f"Recommended Destination Teams for {player}",
    labels={
        "destination_team":"Destination Team",
        "recommendation_score":"Recommendation Score",
        "acceptance_score":"Acceptance Score"
    },
    color_continuous_scale="Viridis")

fig.update_traces(texttemplate="%{text:.2f}")

fig.show()
