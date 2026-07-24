#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 11:35:25 2026

@author: amirreza
"""

from sqltopython import *

query = """

WITH PlayerScores AS
(
    SELECT
        p.player_id,
        p.name,
        p.position,
        p.height,
        AVG(pss.experience) AS experience,

        AVG(
            0.40*per+
            0.30*pts+
            0.15*ast+
            0.10*trb+
            0.05*stl
        ) AS performance_score

    FROM Players p

    JOIN PlayerSeasonStats pss
        ON p.player_id = pss.player_id

    WHERE
        p.position LIKE '%Point Guard%'
        AND pss.season IN ('2020','2021','2022','2023','2024')

    GROUP BY
        p.player_id,
        p.name,
        p.position,
        p.height
),

MJCount AS
(
    SELECT
        aw.player_id,
        COUNT(*) AS mj_appearances

    FROM AwardSeason aw

    JOIN Awards a
        ON aw.award_id=a.award_id

    WHERE a.short_name='MVP'

    GROUP BY aw.player_id
)

SELECT

    ps.name,

    ROUND(ps.performance_score,2) AS performance_score,

    ROUND(ps.experience,1) AS experience,

    ps.height,

    COALESCE(mj.mj_appearances,0) AS mj_appearances,

    DENSE_RANK() OVER
    (
        ORDER BY
            COALESCE(mj.mj_appearances,0) DESC,
            ps.performance_score DESC
    ) ranking

FROM PlayerScores ps

LEFT JOIN MJCount mj

ON ps.player_id=mj.player_id

ORDER BY ranking

LIMIT 15;
"""
#%%
df = run_query(query)

#%%
pio.renderers.default = "browser"

fig = px.scatter(
    df,
    x="performance_score",
    y="mj_appearances",
    size="experience",
    color="ranking",
    text="name",
    size_max=45,
    color_continuous_scale=[
        "#D4AF37",   # Gold
        "#1F4E79",   # Navy
        "#5A5A5A"    # Gray
    ],
    title="Recommended Point Guards Based on MVP Appearances and Performance"
)

fig.update_traces(
    textposition="top center",
    marker=dict(
        line=dict(width=1.5, color="white"),
        opacity=0.9
    )
)

fig.add_annotation(
    x=1.02,
    y=1.08,
    xref="paper",
    yref="paper",
    text="Bubble size ∝ Experience (Years)",
    showarrow=False,
    font=dict(size=13)
)

fig.update_layout(
    template="plotly_white",
    width=950,
    height=600,
    title=dict(
        text="Top 3 Point Guard Recommendations<br><sup>Selection Based on MVP Appearances and Performance Score</sup>",
        x=0.5
    ),
    xaxis_title="Average Performance Score",
    yaxis_title="MVP Appearances",
    font=dict(size=14),
    coloraxis_colorbar=dict(
        title="Rank"
    )
)

fig.show()