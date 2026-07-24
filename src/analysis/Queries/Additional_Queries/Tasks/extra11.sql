-- Q11: Are awards distributed uniformly across different player positions?
select
    p.position,
    aw.short_name as award_name,
    as2.season
from awardseason as2
join players p on as2.player_id = p.player_id
join awards aw on as2.award_id = aw.award_id;