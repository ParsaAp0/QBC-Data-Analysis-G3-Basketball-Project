#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 16:46:39 2026

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
    experience,
    per
FROM BestSeasonRecord;
"""
#%%
#PER Vs Experience
df = run_query(query)
#%%
summary = (df.describe()
      .round(2))

print(summary)
#%%
r, p = pearsonr(
    df["experience"],
    df["per"]
)

print(f"Pearson r = {r:.3f}")
print(f"p-value = {p:.6f}")
#%%
rho, p = spearmanr(
    df["experience"],
    df["per"]
)

print(f"Spearman rho = {rho:.3f}")
print(f"p-value = {p:.6f}")
#%%
pio.renderers.default = "browser"

fig = px.scatter(
    df,
    x="experience",
    y="per",
    trendline="ols",
    opacity=0.55)

fig.update_traces(
    marker=dict(
        size=7,
        color="#1F4E79",
        line=dict(
            width=0.5,
            color="white")))

fig.update_layout(
    template="plotly_white",
    width=900,
    height=600,
    title=dict(
        text="Relationship Between Experience and PER",
        x=0.5
    ),
    xaxis_title="Experience (Years)",
    yaxis_title="Player Efficiency Rating (PER)")

fig.show()
#%%
fig = px.density_heatmap(
    df,
    x="experience",
    y="per",
    nbinsx=20,
    nbinsy=20,
    color_continuous_scale="bluyl"
)

fig.update_layout(
    template="plotly_white",
    width=850,
    height=600,
    title="Density of Experience vs PER"
)

fig.show()
