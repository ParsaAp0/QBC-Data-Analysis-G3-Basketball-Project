-- Q4: Does the win percentage differ between Eastern Conference and Western Conference teams?
select
    t.conference,
    tss.wins / (tss.wins + tss.losses) as win_percentage
from teamseasonstats tss
join teams t on tss.team_id = t.team_id;
