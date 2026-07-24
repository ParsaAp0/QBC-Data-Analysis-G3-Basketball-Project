-- Q18: Player age vs PER
select
    timestampdiff(year, p.birth_date, str_to_date(concat(pss.season, '-01-01'), '%Y-%m-%d')) as age,
    pss.per
from playerseasonstats pss
join players p on pss.player_id = p.player_id;