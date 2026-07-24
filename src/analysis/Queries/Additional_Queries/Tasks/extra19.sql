-- Q19: Player height vs total rebounds
select
    p.height,
    pss.trb
from playerseasonstats pss
join players p on pss.player_id = p.player_id;