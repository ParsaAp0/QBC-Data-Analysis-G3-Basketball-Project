create index idx_players_name
on Players(name);

create index idx_team_name
on Teams(name);

create index idx_player_season
on PlayerSeasonStats(player_id,season);

create index idx_team_season
on PlayerSeasonStats(team_id,season);

create index idx_award_player
on AwardSeason(player_id);

create index idx_award_season
on AwardSeason(season);

create index idx_teamseason
on TeamSeasonStats(team_id,season);