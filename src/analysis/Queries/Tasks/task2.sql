-- Season 2022-2023
-- Champion Team (Denver Nuggets): Experience Distribution
select
    '2022-2023' as Season,
    'Champion Team' as PlayerGroup,
    'Experience' as Metric,
    case
        when pss.experience <= 2 then '0-2'
        when pss.experience <= 5 then '3-5'
        when pss.experience <= 10 then '6-10'
        else '11+'
    end as Category,
    count(*) as count
from PlayerSeasonStats pss
join Teams t on pss.team_id = t.team_id
where pss.season = '2023'
  and t.name = 'Denver Nuggets'
group by Category;

-- Champion Team (Denver Nuggets): Height Distribution
select
    '2022-2023' as Season,
    'Champion Team' as PlayerGroup,
    'Height' as Metric,
    case
        when p.height < 180 then '<180'
        when p.height < 190 then '180-189'
        when p.height < 200 then '190-199'
        when p.height < 210 then '200-209'
        else '210+'
    end as Category,
    count(*) as count
from PlayerSeasonStats pss
join Players p on pss.player_id = p.player_id
join Teams t on pss.team_id = t.team_id
where pss.season = '2023'
  and t.name = 'Denver Nuggets'
group by Category;

-- Top 15 Players: Experience Distribution
select
    '2022-2023' as Season,
    'Top 15' as PlayerGroup,
    'Experience' as Metric,
    case
        when pss.experience <= 2 then '0-2'
        when pss.experience <= 5 then '3-5'
        when pss.experience <= 10 then '6-10'
        else '11+'
    end as Category,
    count(*) as count
from PlayerSeasonStats pss
where pss.season = '2023'
  and pss.player_id in (
    select player_id
    from (
        select
            player_id,
            row_number() over(
                order by (0.40 * per + 0.30 * pts + 0.15 * ast + 0.10 * trb + 0.05 * stl) desc
            ) rn
        from PlayerSeasonStats
        where season = '2023'
    ) ranked
    where rn <= 15
)
group by Category;

-- Top 15 Players: Height Distribution
select
    '2022-2023' as Season,
    'Top 15' as PlayerGroup,
    'Height' as Metric,
    case
        when p.height < 180 then '<180'
        when p.height < 190 then '180-189'
        when p.height < 200 then '190-199'
        when p.height < 210 then '200-209'
        else '210+'
    end as Category,
    count(*) as count
from Players p
where p.player_id in (
    select player_id
    from (
        select
            player_id,
            row_number() over(
                order by (0.40 * per + 0.30 * pts + 0.15 * ast + 0.10 * trb + 0.05 * stl) desc
            ) rn
        from PlayerSeasonStats
        where season = '2023'
    ) ranked
    where rn <= 15
)
group by Category;

-- Season 2023-2024
-- Champion Team (Boston Celtics): Experience Distribution
select
    '2023-2024' as Season,
    'Champion Team' as PlayerGroup,
    'Experience' as Metric,
    case
        when pss.experience <= 2 then '0-2'
        when pss.experience <= 5 then '3-5'
        when pss.experience <= 10 then '6-10'
        else '11+'
    end as Category,
    count(*) as count
from PlayerSeasonStats pss
join Teams t on pss.team_id = t.team_id
where pss.season = '2024'
  and t.name = 'Boston Celtics'
group by Category;

-- Champion Team (Boston Celtics): Height Distribution
select
    '2023-2024' as Season,
    'Champion Team' as PlayerGroup,
    'Height' as Metric,
    case
        when p.height < 180 then '<180'
        when p.height < 190 then '180-189'
        when p.height < 200 then '190-199'
        when p.height < 210 then '200-209'
        else '210+'
    end as Category,
    count(*) as count
from PlayerSeasonStats pss
join Players p on pss.player_id = p.player_id
join Teams t on pss.team_id = t.team_id
where pss.season = '2024'
  and t.name = 'Boston Celtics'
group by Category;

-- Top 15 Players: Experience Distribution
select
    '2023-2024' as Season,
    'Top 15' as PlayerGroup,
    'Experience' as Metric,
    case
        when pss.experience <= 2 then '0-2'
        when pss.experience <= 5 then '3-5'
        when pss.experience <= 10 then '6-10'
        else '11+'
    end as Category,
    count(*) as count
from PlayerSeasonStats pss
where pss.season = '2024'
  and pss.player_id in (
    select player_id
    from (
        select
            player_id,
            row_number() over(
                order by (0.40 * per + 0.30 * pts + 0.15 * ast + 0.10 * trb + 0.05 * stl) desc
            ) rn
        from PlayerSeasonStats
        where season = '2024'
    ) ranked
    where rn <= 15
)
group by Category;

-- Top 15 Players: Height Distribution
select
    '2023-2024' as Season,
    'Top 15' as PlayerGroup,
    'Height' as Metric,
    case
        when p.height < 180 then '<180'
        when p.height < 190 then '180-189'
        when p.height < 200 then '190-199'
        when p.height < 210 then '200-209'
        else '210+'
    end as Category,
    count(*) as count
from Players p
where p.player_id in (
    select player_id
    from (
        select
            player_id,
            row_number() over(
                order by (0.40 * per + 0.30 * pts + 0.15 * ast + 0.10 * trb + 0.05 * stl) desc
            ) rn
        from PlayerSeasonStats
        where season = '2024'
    ) ranked
    where rn <= 15
)
group by Category;
