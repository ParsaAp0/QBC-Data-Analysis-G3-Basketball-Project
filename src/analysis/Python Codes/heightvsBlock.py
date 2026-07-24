#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 19:09:30 2026

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
                PARTITION BY pss.player_id, pss.season
                ORDER BY pss.minutes DESC
            ) AS rn
        FROM PlayerSeasonStats pss
        WHERE pss.games >= 20
    ) t
    WHERE rn = 1
)

SELECT
    p.height,
    bsr.blk
FROM BestSeasonRecord bsr
JOIN Players p
    ON bsr.player_id = p.player_id
WHERE
    p.height IS NOT NULL
    AND bsr.blk IS NOT NULL;
"""
#%%
df = run_query(query)
#%%
summary = df.describe().round(2)

print(summary)
#%%

r, p = pearsonr(df["height"], df["blk"])

print(f"Pearson r = {r:.3f}")
print(f"p-value = {p:.6f}")
#%%

rho, p = spearmanr(
    df["height"],
    df["blk"]
)

print(f"Spearman rho = {rho:.3f}")
print(f"p-value = {p:.6f}")
#%%
summary = (
    df.groupby("height")
      .agg(
          MeanBlocks=("blk", "mean"),
          Count=("blk", "size"))
      .reset_index())

fig = px.scatter(
    summary,
    x="height",
    y="MeanBlocks",
    size="Count",
    color="Count",
    color_continuous_scale=[
        "#D4AF37",
        "#1F4E79"
    ],
    size_max=35)

fig.update_traces(
    marker=dict(
        line=dict(color="white", width=1)))

fig.update_layout(
    template="plotly_white",
    title="Average Blocks by Player Height",
    xaxis_title="Height (cm)",
    yaxis_title="Average Blocks per Game",
    coloraxis_colorbar_title="Players")

fig.show()