#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 16:21:56 2026

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

    aw.short_name AS Award,

    as2.season

FROM AwardSeason as2

JOIN Players p
    ON as2.player_id = p.player_id

JOIN Awards aw
    ON as2.award_id = aw.award_id;
    """
    
#%%
df = run_query(query)
#%%
summary = (df.groupby(["Position","Award"])
      .size()
      .reset_index(name="Count"))

print(summary)
#%%
table = pd.crosstab(
    df["Position"],
    df["Award"])

print(table)
#%%
chi2, p, dof, expected = chi2_contingency(table)

print(f"Chi-square = {chi2:.3f}")
print(f"df = {dof}")
print(f"p-value = {p:.6f}")
#%%
n = table.values.sum()

k = min(table.shape)

cramers_v = np.sqrt(chi2 / (n * (k - 1)))

print(f"Cramer's V = {cramers_v:.3f}")
#%%
fig = px.imshow(
    table,
    text_auto=True,
    color_continuous_scale=[
        "#F8F4E3",
        "#D4AF37",
        "#1F4E79"
    ]
,
    aspect="auto"
)

fig.update_layout(
    template="plotly_white",
    width=900,
    height=600,
    title=dict(
        text="Distribution of Awards Across Player Positions",
        x=0.5
    ),
    xaxis_title="Award",
    yaxis_title="Position"
)

fig.show()
#%%
fig = px.histogram(
    df,
    x="Award",
    color="Position",
    barmode="group",
    color_discrete_sequence=[
        "#1F4E79",
        "#4C78A8",
        "#D4AF37",
        "#E07A5F",
        "#7A5195"
    ]
)

fig.update_layout(
    template="plotly_white",
    width=950,
    height=600,
    title=dict(
        text="Award Counts by Player Position",
        x=0.5
    ),
    xaxis_title="Award",
    yaxis_title="Number of Awards"
)

fig.show()
#%%
percentage = (
    table.div(table.sum(axis=0), axis=1)
         .reset_index()
         .melt(
             id_vars="Position",
             var_name="Award",
             value_name="Percentage"
         )
)

fig = px.bar(
    percentage,
    x="Award",
    y="Percentage",
    color="Position",
    barmode="relative",
    color_discrete_sequence=[
        "#1F4E79",
        "#4C78A8",
        "#D4AF37",
        "#E07A5F",
        "#7A5195"
    ]
)

fig.update_yaxes(tickformat=".0%")

fig.update_layout(
    template="plotly_white",
    width=950,
    height=600,
    title=dict(
        text="Relative Distribution of Awards by Position",
        x=0.5
    )
)

fig.show()