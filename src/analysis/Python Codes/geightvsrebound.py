#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 19:01:40 2026

@author: amirreza
"""

from sqltopython import*

query = """
WITH BestSeasonRecord AS
(
    SELECT *
    FROM
    (
        SELECT
            pss.*,
            ROW_NUMBER() OVER
            (
                PARTITION BY player_id, season
                ORDER BY minutes DESC
            ) AS rn
        FROM PlayerSeasonStats pss
        WHERE games >= 20
    ) t
    WHERE rn = 1
)

SELECT
    p.height,
    bsr.trb AS rebounds
FROM BestSeasonRecord bsr
JOIN Players p
    ON bsr.player_id = p.player_id;
    """
#%%
#Height vs rebound
df = run_query(query)
#%%
from scipy.stats import pearsonr

r, p = pearsonr(
    df["height"],
    df["rebounds"]
)

print(f"Pearson r = {r:.3f}")
print(f"p-value = {p:.6f}")
#%%
result = linregress(
    df["height"],
    df["rebounds"])

print(result)
#%%

pio.renderers.default = "browser"

fig = px.scatter(
    df,
    x="height",
    y="rebounds",
    trendline="ols",
    opacity=0.55,
    color_discrete_sequence=["#1F4E79"]
)

fig.update_traces(
    marker=dict(
        size=7,
        line=dict(
            color="white",
            width=0.8
        )
    )
)

fig.update_layout(
    template="plotly_white",
    width=900,
    height=600,
    title=dict(
        text="Relationship Between Player Height and Rebounds",
        x=0.5
    ),
    xaxis_title="Height (cm)",
    yaxis_title="Total Rebounds per Game",
    font=dict(size=14),
    showlegend=False
)

fig.show()
#%%
plot_df = df.copy()

plot_df["HeightGroup"] = pd.cut(
    plot_df["height"],
    bins=range(175,231,5)
)

fig = px.box(
    plot_df,
    x="HeightGroup",
    y="rebounds",
    color="HeightGroup",
    color_discrete_sequence=["#1F4E79"]
)

fig.update_layout(
    template="plotly_white",
    width=950,
    height=600,
    title=dict(
        text="Rebound Distribution Across Height Groups",
        x=0.5
    ),
    xaxis_title="Height Group (cm)",
    yaxis_title="Rebounds",
    showlegend=False
)

fig.show()