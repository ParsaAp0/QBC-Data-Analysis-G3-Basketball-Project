-- Q20: Player height vs blocks
select
    p.height,
    pss.blk
from playerseasonstats pss
join players p on pss.player_id = p.player_id;