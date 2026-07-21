#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 10:43:03 2026

@author: amirreza
"""

from sqltopython import *
#%%
query = """
WITH JordanPlayers AS
(
    SELECT DISTINCT as2.player_id
    FROM AwardSeason as2
    JOIN Awards a
        ON as2.award_id = a.award_id
    WHERE a.short_name = 'MVP'
),

Top50Players AS
(
    SELECT player_id
    FROM
    (
        SELECT
            player_id,
            ROW_NUMBER() OVER
            (
                ORDER BY
                    (0.40 * per +
                     0.30 * pts +  # Increase this value
                     0.15 * ast +
                     0.10 * trb +
                     0.05 * stl) DESC
            ) AS rn
        FROM PlayerSeasonStats
        WHERE season BETWEEN '2020' AND '2024'
    ) ranked
    WHERE rn <= 50
)

SELECT
    p.height,
    'Michael Jordan Trophy' AS PlayerGroup
FROM Players p
WHERE p.player_id IN (SELECT player_id FROM JordanPlayers)

UNION ALL

SELECT
    p.height,
    'Top 50 Players' AS PlayerGroup
FROM Players p
WHERE p.player_id IN (SELECT player_id FROM Top50Players);
"""
#%%
df = run_query(query)
#%%
#Report
summary = (
    df.groupby("PlayerGroup")
    ["height"]
    .agg(["mean","median","std"])
    .reset_index())

summary
#%%
import plotly.express as px
import plotly.io as pio

pio.renderers.default = "browser"

color_map = {
    "Michael Jordan Trophy": "#D4AF37",
    "Top 50 Players": "#1F4E79"
}

fig = px.violin(
    df,
    x="PlayerGroup",
    y="height",
    color="PlayerGroup",
    color_discrete_map=color_map,
    box=True,
    points="all",
    title="Height Distribution of Elite NBA Players",
)

fig.update_traces(
    meanline_visible=True,
    marker=dict(
        size=7,
        opacity=0.65
    )
)

fig.update_layout(
    template="plotly_white",
    width=900,
    height=600,
    title={
        "text": "Height Distribution of Elite NBA Players<br><sup>MVP Winners vs Top 50 Players (2020-2024)</sup>",
        "x":0.5,
        "xanchor":"center"
    },
    xaxis_title="",
    yaxis_title="Height (cm)",
    font=dict(
        family="Arial",
        size=14
    ),
    legend_title_text="Player Group",
    showlegend=False
)

fig.show()
#%%
fig = px.histogram(
    df,
    x="height",
    color="PlayerGroup",
    nbins=10,
    barmode="overlay",
    opacity=0.65,
    color_discrete_map=color_map,
    title="Height Distribution Comparison"
)

fig.update_layout(
    template="plotly_white",
    width=900,
    height=600,
    title={
        "text": "Height Distribution Comparison<br><sup>MVP Winners vs Top 50 Players (2020-2024)</sup>",
        "x":0.5,
        "xanchor":"center"
    },
    xaxis_title="Height (cm)",
    yaxis_title="Number of Players",
    font=dict(
        family="Arial",
        size=14
    ),
    legend_title_text="Player Group",
)

fig.update_traces(
    marker_line_width=1,
    marker_line_color="white"
)

fig.show()