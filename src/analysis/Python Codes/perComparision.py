#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 14:55:15 2026

@author: amirreza
"""

from sqltopython import*


query = """
SELECT
    TRIM(
        SUBSTRING_INDEX(
            REPLACE(
                REPLACE(p.position,' and ',','),
                '/',
                ','
            ),
            ',',
            1
        )
    ) AS Position,

    pss.per

FROM PlayerSeasonStats pss

JOIN Players p
ON pss.player_id = p.player_id

WHERE pss.per IS NOT NULL;
"""
#%%
per_df = run_query(query)
#%%
summary = (
    per_df.groupby("Position")["per"]
      .agg(
          Count="count",
          Mean="mean",
          Median="median",
          Std="std",
          Min="min",
          Max="max"
      )
      .round(2))

print(summary)
#%%

for pos in sorted(per_df["Position"].unique()):
    w, p = shapiro(per_df[per_df["Position"] == pos]["per"])
    print(f"{pos:18s} W={w:.4f}  p={p:.4f}")

#%%

F, p = f_oneway(*groups)

print(F, p)
#%%
grand_mean = per_df["per"].mean()

ss_between = sum(
    len(g)*(g.mean()-grand_mean)**2
    for _, g in per_df.groupby("Position")["per"]
)

ss_total = ((per_df["per"]-grand_mean)**2).sum()

eta2 = ss_between / ss_total

print("Eta squared =", eta2)
#%%


tukey = pairwise_tukeyhsd(
    endog=per_df["per"],
    groups=per_df["Position"],
    alpha=0.05
)

print(tukey)
#%%

pio.renderers.default = "browser"

color_map = {
    "Center": "#1F4E79",
    "Power Forward": "#4C78A8",
    "Small Forward": "#D4AF37",
    "Shooting Guard": "#E07A5F",
    "Point Guard": "#7A5195"}

fig = px.violin(
    per_df,
    x="Position",
    y="per",
    color="Position",
    color_discrete_map=color_map,
    box=True,
    points="all")

fig.update_traces(
    meanline_visible=True,
    marker=dict(size=4, opacity=0.45))

fig.update_layout(
    template="plotly_white",
    width=950,
    height=600,
    title=dict(
        text="PER Distribution Across Player Positions",
        x=0.5
    ),
    xaxis_title="Primary Position",
    yaxis_title="Player Efficiency Rating (PER)",
    showlegend=False,
    font=dict(size=14))

fig.show()