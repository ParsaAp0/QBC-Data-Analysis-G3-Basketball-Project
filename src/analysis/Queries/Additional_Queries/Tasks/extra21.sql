-- Q21: Player assists vs team wins
select
    pss.ast,
    tss.wins
from playerseasonstats pss
join teamseasonstats tss on pss.team_id = tss.team_id and pss.season = tss.season;