with JordanPlayers as
(
    select distinct as2.player_id
    from AwardSeason as2
    join Awards a
        on as2.award_id = a.award_id
    where a.short_name = 'MVP'
),

Top50Players as
(
    select player_id
    from
    (
        select
            player_id,
            row_number() over(
                order by (0.40 * per + 0.30 * pts + 0.15 * ast + 0.10 * trb + 0.05 * stl) desc
            ) rn
        from PlayerSeasonStats
        where season between '2020' and '2024'
    ) ranked
    where rn <= 50
)

select
    'Michael Jordan Trophy' as PlayerGroup,

    case
        when p.height < 180 then '<180'
        when p.height < 190 then '180-189'
        when p.height < 200 then '190-199'
        when p.height < 210 then '200-209'
        else '210+'
    end as HeightRange,

    count(*) as TotalPlayers

from Players p
where p.player_id in (select player_id from JordanPlayers)
group by HeightRange

union all

select
    'Top50' as PlayerGroup,

    case
        when p.height < 180 then '<180'
        when p.height < 190 then '180-189'
        when p.height < 200 then '190-199'
        when p.height < 210 then '200-209'
        else '210+'
    end as HeightRange,

    count(*) as TotalPlayers

from Players p
where p.player_id in (select player_id from Top50Players)
group by HeightRange;