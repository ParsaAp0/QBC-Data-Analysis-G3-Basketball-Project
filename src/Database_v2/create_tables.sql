use basketball_db;

-- PLAYERS
create table Players
(
    player_id int primary key,

    name varchar(120) not null,

    birth_date date,

    height decimal(5,2),

    weight decimal(5,2),

    nationality varchar(80),

    position varchar(60),

    shoots varchar(20),

    college varchar(150),

    draft_year int,

    draft_round int,

    draft_pick int,

    draft_team varchar(100)
);


-- TEAMS
create table Teams
(
    team_id int primary key,

    name varchar(100) not null,

    franchise varchar(100),

    conference varchar(50),

    division varchar(50),

    short_name varchar(20)
);

-- AWARDS
create table Awards
(
    award_id int primary key,

    short_name varchar(100),

    trophy_name varchar(150),

    description text
);

-- PLAYER SEASON STATS
create table PlayerSeasonStats
(
    player_id int not null,

    team_id int not null,

    season varchar(20) not null,

    position varchar(60) not null,

    experience int,

    games int,

    games_started int,

    minutes decimal(8,2),

    fg decimal(8,2),

    fga decimal(8,2),

    fg_percent decimal(5,3),

    three_p decimal(8,2),

    three_pa decimal(8,2),

    three_percent decimal(5,3),

    two_p decimal(8,2),

    two_pa decimal(8,2),

    two_percent decimal(5,3),

    efg decimal(5,3),

    ft decimal(8,2),

    fta decimal(8,2),

    ft_percent decimal(5,3),

    orb decimal(8,2),

    drb decimal(8,2),

    trb decimal(8,2),

    ast decimal(8,2),

    stl decimal(8,2),

    blk decimal(8,2),

    tov decimal(8,2),

    pf decimal(8,2),

    pts decimal(8,2),

    per decimal(8,2),

    primary key(player_id,team_id,season),

    foreign key(player_id)
        references Players(player_id),

    foreign key(team_id)
        references Teams(team_id)
);

-- TEAM SEASON STATS
create table TeamSeasonStats
(
    team_id int not null,

    season varchar(20) not null,

    games int,

    wins int,

    losses int,

    `W/L%` float,

    standing int,

    conference_standing int,

    playoff_result varchar(50),

    conference_champion boolean,

    champion boolean,

    MP float,

    pace float,

    relative_pace float,

    ORtg float,

    relative_ORtg float,

    DRtg float,

    relative_DRtg float,

    `Pts/G` int,

    `Opp Pts/G` float,

    fg int,

    fga int,

    `fg%` float,

    3p int,

    3pa int,

    `3p%` float,

    2p int,

    2pa int,

    `2p%` float,

    `eFG%` float,

    ft int,

    fta int,

    `ft%` float,

    `ft/fga` float,

    orb int,

    `orb%` float,

    drb int,

    `drb%` float,

    trb int,

    `trb/G` float,

    ast int,

    `ast/G` float,

    stl int,

    `stl/G` float,

    blk int,

    `blk/G` float,

    tov int,

    `tov/G` float,

    fouls int,

    `fouls/G` float,

    primary key(team_id,season),

    foreign key(team_id)
        references Teams(team_id)
);


-- AWARD SEASON
create table AwardSeason
(
    award_id int not null,

    player_id int not null,

    season varchar(20) not null,

    primary key
    (
        award_id,
        player_id,
        season
    ),

    foreign key(award_id)
        references Awards(award_id),

    foreign key(player_id)
        references Players(player_id)
);