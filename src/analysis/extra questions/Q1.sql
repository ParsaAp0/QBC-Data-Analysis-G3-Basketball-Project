SELECT Teams.name as Name,
       TSS.*,
       CASE
           WHEN TSS.standing <= 5 THEN 'Top 5'
           ELSE 'Down 15'
           END    as rating
from Teams
         join TeamSeasonStats TSS on Teams.team_id = TSS.team_id
where (TSS.standing >= 15 or TSS.standing < 6)# and TSS.season = "2021"
order by TSS.Season, TSS.standing;

# If we specify the season, we would have only 5 data for `top 5` teams which is not ideal.