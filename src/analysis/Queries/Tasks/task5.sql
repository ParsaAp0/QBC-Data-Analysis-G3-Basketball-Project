select
    case pss.season
        when '2020' then '2019-2020'
        when '2021' then '2020-2021'
        when '2022' then '2021-2022'
        when '2023' then '2022-2023'
        when '2024' then '2023-2024'
    end as Season,

    t.name as ChampionTeam,

    p.name as PlayerName,

    cast(pss.season as unsigned) - year(p.birth_date) as Age,

    pss.experience as Experience,

    round(
        pss.experience /
        (cast(pss.season as unsigned) - year(p.birth_date)),
        4
    ) as InnateAbility

from PlayerSeasonStats pss

join Players p
    on pss.player_id = p.player_id

join Teams t
    on pss.team_id = t.team_id

join TeamSeasonStats tss
    on t.team_id = tss.team_id
   and pss.season = tss.season

where
    tss.champion = TRUE
    and pss.season in ('2020','2021','2022','2023','2024')

order by
    cast(pss.season as unsigned),
    PlayerName;