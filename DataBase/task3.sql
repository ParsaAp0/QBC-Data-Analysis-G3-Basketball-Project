with MJ_Appearances as
(
    select
        p.player_id,
        p.name,
        count(*) as mj_appearances
    from AwardSeason aw
    join Awards a
        on aw.award_id = a.award_id
    join Players p
        on aw.player_id = p.player_id
    where a.short_name = 'MVP'
      and aw.season in ('2019-20','2020-21','2021-22','2022-23','2023-24')
      and p.position like '%Point Guard%'
    group by p.player_id, p.name
),

TopScores as
(
    select
        player_id,

        avg(
            0.40 * per +
            0.30 * pts +
            0.15 * ast +
            0.10 * trb +
            0.05 * stl
        ) as avg_top_score

    from PlayerSeasonStats

    where season in ('2020','2021','2022','2023','2024')

    group by player_id
)

select

    m.name,

    m.mj_appearances,

    round(t.avg_top_score,2) as avg_top_score,

    rank() over
    (
        order by
            m.mj_appearances desc,
            t.avg_top_score desc
    ) as ranking

from MJ_Appearances m

join TopScores t

on m.player_id = t.player_id

order by

    m.mj_appearances desc,

    t.avg_top_score desc

limit 3;