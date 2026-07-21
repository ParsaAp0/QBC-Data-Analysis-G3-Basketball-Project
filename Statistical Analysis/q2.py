#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 11:24:32 2026

@author: amirreza
"""

from sqltopython import *

query = """
WITH Top15 AS
(
    SELECT
        season,
        player_id
    FROM
    (
        SELECT
            season,
            player_id,
            ROW_NUMBER() OVER
            (
                PARTITION BY season
                ORDER BY
                    (0.40 * per +
                     0.30 * pts +
                     0.15 * ast +
                     0.10 * trb +
                     0.05 * stl) DESC
            ) AS rn
        FROM PlayerSeasonStats
        WHERE season IN ('2023','2024')
    ) ranked
    WHERE rn <= 15
),

ChampionTeams AS
(
    SELECT
        ts.season,
        ts.team_id,
        t.name AS team_name
    FROM TeamSeasonStats ts
    JOIN Teams t
        ON ts.team_id = t.team_id
    WHERE
        ts.champion = TRUE
        AND ts.season IN ('2023','2024')
)

-- Champion team players
SELECT
    CASE
        WHEN pss.season='2023' THEN '2022-2023'
        WHEN pss.season='2024' THEN '2023-2024'
    END AS Season,

    'Champion Team' AS PlayerGroup,

    p.player_id,
    p.name,

    p.height,
    pss.experience

FROM PlayerSeasonStats pss

JOIN Players p
    ON p.player_id = pss.player_id

JOIN ChampionTeams ct
    ON ct.team_id = pss.team_id
   AND ct.season = pss.season

UNION ALL

-- Top 15 players
SELECT

    CASE
        WHEN pss.season='2023' THEN '2022-2023'
        WHEN pss.season='2024' THEN '2023-2024'
    END AS Season,

    'Top 15' AS PlayerGroup,

    p.player_id,
    p.name,

    p.height,
    pss.experience

FROM PlayerSeasonStats pss

JOIN Players p
    ON p.player_id = pss.player_id

JOIN Top15 tp
    ON tp.player_id = pss.player_id
   AND tp.season = pss.season

ORDER BY
    Season,
    PlayerGroup,
    height;
"""
#%%
df = run_query(query)
#%%
height_summary = (
    df.groupby(["Season", "PlayerGroup"])["height"]
      .agg(
          Count="count",
          Mean="mean",
          Median="median",
          Std="std",
          Min="min",
          Max="max"
      )
      .round(2)
      .reset_index()
)

print(height_summary)
#%%
experience_summary = (
    df.groupby(["Season", "PlayerGroup"])["experience"]
      .agg(
          Count="count",
          Mean="mean",
          Median="median",
          Std="std",
          Min="min",
          Max="max"
      )
      .round(2)
      .reset_index()
)

print(experience_summary)
#%%
bins = [-1, 2, 5, 10, 100]

labels = [
    "0-2",
    "3-5",
    "6-10",
    "11+"
]

df["ExperienceGroup"] = pd.cut(
    df["experience"],
    bins=bins,
    labels=labels
)
#%%
experience_distribution = (

    df
    .groupby(
        ["Season",
         "PlayerGroup",
         "ExperienceGroup"]
    )
    .size()
    .reset_index(name="Count")

)
#%%
experience_distribution["Percentage"] = (

    experience_distribution
    .groupby(["Season","PlayerGroup"])["Count"]
    .transform(lambda x: 100*x/x.sum())

)

#%%

experience["Percentage"] = (
    experience
    .groupby(["Season", "PlayerGroup"])["Count"]
    .transform(lambda x: 100*x/x.sum())
)
#%%
import plotly.express as px

color_map = {
    "Champion Team": "#D4AF37",
    "Top 15": "#1F4E79"
}

for season in sorted(df["Season"].unique()):

    temp = df[df["Season"] == season]

    fig = px.violin(
        temp,
        x="PlayerGroup",
        y="height",
        color="PlayerGroup",
        color_discrete_map=color_map,
        box=True,
        points="all",
        title=f"Height Distribution ({season})"
    )

    fig.update_traces(
        meanline_visible=True,
        marker=dict(size=7, opacity=0.65)
    )

    fig.update_layout(
        template="plotly_white",
        width=850,
        height=600,
        title=dict(
            text=f"Height Distribution Comparison<br><sup>{season}</sup>",
            x=0.5
        ),
        yaxis_title="Height (cm)",
        xaxis_title="",
        showlegend=False,
        font=dict(size=14)
    )

    fig.show()
#%%
import plotly.express as px

color_map = {
    "Champion Team": "#D4AF37",
    "Top 15": "#1F4E79"
}

for season in sorted(experience["Season"].unique()):

    temp = experience[
        experience["Season"] == season
    ]

    fig = px.bar(
        temp,
        x="ExperienceGroup",
        y="Percentage",
        color="PlayerGroup",
        barmode="group",
        text=temp["Percentage"].round(1),
        color_discrete_map=color_map
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    fig.update_layout(
        template="plotly_white",
        width=850,
        height=600,
        title=dict(
            text=f"Experience Distribution Comparison<br><sup>{season}</sup>",
            x=0.5
        ),
        xaxis_title="Experience (Years)",
        yaxis_title="Percentage (%)",
        yaxis=dict(range=[0,100]),
        font=dict(size=14)
    )

    fig.show()








