-- Q8: Does PER differ among player positions?
select
    p.position,
    pss.per
from playerseasonstats pss
join players p on pss.player_id = p.player_id;