#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 11:35:27 2026

@author: amirreza
"""

from sqltopython import *

query = """
with BestSeasonRecord as
(
    select *
    from
    (
        select
            pss.*,
            row_number() over
            (
                partition by pss.player_id, pss.season
                order by pss.minutes desc
            ) as rn
        from PlayerSeasonStats pss
        where
            pss.season in ('2021','2022','2023','2024')
            and pss.games >= 20
    ) t
    where rn = 1
),

RankedPlayers as
(
    select

        case bsr.season
            when '2021' then '2020-2021'
            when '2022' then '2021-2022'
            when '2023' then '2022-2023'
            when '2024' then '2023-2024'
        end as Season,

        p.name as PlayerName,

        p.height as Height,

        p.weight as Weight,

        round(p.height / p.weight,4) as Agility,

        round
        (
            0.40 * bsr.per +
            0.30 * bsr.pts +
            0.15 * bsr.ast +
            0.10 * bsr.trb +
            0.05 * bsr.stl,
            2
        ) as TopPlayerScore,

        row_number() over
        (
            partition by bsr.season
            order by
            (
                0.40 * bsr.per +
                0.30 * bsr.pts +
                0.15 * bsr.ast +
                0.10 * bsr.trb +
                0.05 * bsr.stl
            ) desc
        ) as SeasonRank

    from BestSeasonRecord bsr
    join Players p
        on bsr.player_id = p.player_id
)

select
    Season,
    PlayerName,
    Height,
    Weight,
    Agility,
    TopPlayerScore
from RankedPlayers
where SeasonRank <= 20
order by Season, TopPlayerScore desc;
"""
#%%

df = run_query(query)
#%%
old = df[df["Season"].isin(
    ["2020-2021","2021-2022"]
)]["Agility"]

new = df[df["Season"].isin(
    ["2022-2023","2023-2024"]
)]["Agility"]
#%%

summary = df.groupby("Season")["Agility"].agg(
    ["count","mean","median","std","min","max"]
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
n1=len(old)
n2=len(new)

z=(u-n1*n2/2)/np.sqrt(n1*n2*(n1+n2+1)/12)

r=abs(z)/np.sqrt(n1+n2)

print(r)
#%%
import plotly.express as px
import plotly.io as pio

pio.renderers.default = "browser"

plot_df = df.copy()

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
    y="Agility",
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
    yaxis_title="Agility Index (Height / Weight)",
    font=dict(size=14),
    showlegend=False
)

fig.show()
