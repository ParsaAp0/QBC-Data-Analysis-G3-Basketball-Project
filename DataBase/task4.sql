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