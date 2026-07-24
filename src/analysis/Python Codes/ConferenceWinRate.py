#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 10:31:30 2026

@author: amirreza
"""

#Extra q4 - Does the win percentage differ between Eastern Conference and Western Conference teams?

from sqltopython import*

query = """

SELECT
    t.conference,
    ROUND(
        tss.wins * 1.0 /
        NULLIF(tss.wins + tss.losses,0),
        3
    ) AS win_percentage
FROM TeamSeasonStats tss
JOIN Teams t
    ON tss.team_id = t.team_id;

"""
#%%
df = run_query(query)
#%%
summary = (
    df.groupby("conference")["win_percentage"]
      .agg(
          Count="count",
          Mean="mean",
          Median="median",
          Std="std",
          Min="min",
          Max="max"
      )
      .round(3)
)

print(summary)
#%%
east = df[df["conference"]=="Eastern Conference"]["win_percentage"]
west = df[df["conference"]=="Western Conference"]["win_percentage"]
#%%
for name, group in [("East", east), ("West", west)]:
    W, p = shapiro(group)

    print(name)
    print("W =", round(W,4))
    print("p =", round(p,4))

    if p > 0.05:
        print("Distribution appears normal.\n")
    else:
        print("Distribution is not normal.\n")

#%%
u, p = mannwhitneyu(
    east,
    west,
    alternative="two-sided"
)

print("U =", u)
print("p =", p)
#%%
nx = len(east)
ny = len(west)

pooled = np.sqrt(((nx-1)*east.var(ddof=1)+(ny-1)*west.var(ddof=1))/(nx+ny-2))

d = (east.mean()-west.mean())/pooled

print("Cohen's d =", d)
#%%
fig = px.box(
    df,
    x="conference",
    y="win_percentage",
    color="conference",
    points="all",
    color_discrete_map=color_map)

fig.update_traces(
    jitter=0.25,
    pointpos=-1.6,
    marker=dict(size=5, opacity=0.65),
    line=dict(width=2),
    boxmean=True)

fig.update_layout(
    template="plotly_white",
    width=900,
    height=600,
    title=dict(
        text="<b>Winning Percentage by Conference</b>",
        x=0.5
    ),
    xaxis_title="Conference",
    yaxis_title="Winning Percentage",
    showlegend=False,
    font=dict(size=14))

fig.show()