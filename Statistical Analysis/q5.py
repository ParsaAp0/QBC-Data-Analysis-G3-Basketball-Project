#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 11:35:28 2026

@author: amirreza
"""

from sqltopython import *

query = """
with BestSeasonRecord AS
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
            ) rn

        FROM PlayerSeasonStats pss

        WHERE
            season IN ('2020','2021','2022','2023','2024')
            AND games >= 20

    ) t

    WHERE rn=1
)

SELECT

CASE b.season
    WHEN '2020' THEN '2019-2020'
    WHEN '2021' THEN '2020-2021'
    WHEN '2022' THEN '2021-2022'
    WHEN '2023' THEN '2022-2023'
    WHEN '2024' THEN '2023-2024'
END AS Season,

t.name AS ChampionTeam,

p.name AS PlayerName,

CAST(b.season AS UNSIGNED) - YEAR(p.birth_date) AS Age,

b.experience,

ROUND(
    b.experience /
    NULLIF(
        CAST(b.season AS UNSIGNED) - YEAR(p.birth_date),
        0
    ),
    4
) AS InnateAbility

FROM BestSeasonRecord b

JOIN Players p
ON b.player_id=p.player_id

JOIN Teams t
ON b.team_id=t.team_id

JOIN TeamSeasonStats ts
ON b.team_id=ts.team_id
AND b.season=ts.season

WHERE ts.champion=TRUE

ORDER BY season,PlayerName;
"""
#%%
df = run_query(query)
#%%
old = df[df["Season"].isin(
    ["2020-2021","2021-2022"]
)]["InnateAbility"]

new = df[df["Season"].isin(
    ["2022-2023","2023-2024"]
)]["InnateAbility"]
#%%
summary = (
    df.groupby("Season")["InnateAbility"]
      .agg(["count","mean","median","std","min","max"])
)

print(summary)
#%%
print("Old Mean :", old.mean())
print("New Mean :", new.mean())
#%%

from scipy.stats import shapiro

for name, sample in [
    ("2020-2022", old),
    ("2022-2024", new)
]:
    stat, p = shapiro(sample)

    print(f"\n{name}")
    print(f"W = {stat:.4f}")
    print(f"p = {p:.4f}")

    if p > 0.05:
        print("Distribution appears normal.")
    else:
        print("Distribution is not normal.")

#%%
from scipy.stats import ttest_ind

t_stat, p = ttest_ind(
    old,
    new,
    equal_var=False   
)

print("t =", t_stat)
print("p =", p)
#%%
import numpy as np

n1 = len(old)
n2 = len(new)

z = (u - n1*n2/2) / np.sqrt(n1*n2*(n1+n2+1)/12)

r = abs(z) / np.sqrt(n1+n2)

print("Effect size (r) =", r)


#%%
import plotly.express as px
import plotly.io as pio

pio.renderers.default = "browser"

plot_df = df[
    df["Season"].isin([
        "2020-2021",
        "2021-2022",
        "2022-2023",
        "2023-2024"
    ])
].copy()

plot_df["Period"] = plot_df["Season"].replace({
    "2020-2021": "2020-2022",
    "2021-2022": "2020-2022",
    "2022-2023": "2022-2024",
    "2023-2024": "2022-2024"
})

color_map = {
    "2020-2022": "#1F4E79",
    "2022-2024": "#D4AF37"
}

fig = px.violin(
    plot_df,
    x="Period",
    y="InnateAbility",
    color="Period",
    color_discrete_map=color_map,
    box=True,
    points="all"
)

fig.update_traces(
    meanline_visible=True,
    marker=dict(size=7, opacity=0.65)
)

fig.update_layout(
    template="plotly_white",
    width=900,
    height=600,
    title=dict(
        text="Comparison of Agility Index Between Two Time Periods",
        x=0.5
    ),
    xaxis_title="Period",
    yaxis_title="Innate Ability (Experience / Age)",
    font=dict(size=14),
    showlegend=False
)

fig.show()










