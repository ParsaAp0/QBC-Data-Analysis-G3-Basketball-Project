from db_connection import Database
from pathlib import Path
import pandas as pd
import re
import os
from typing import Type
from datetime import datetime

from models import Team, Conference, Division, TeamSeason, Season, Arena, PlayoffResult, Award, Player, Nationality, Position, PlayerPosition, College, Draft, PlayerSeason, PlayerSeasonAward


def get_or_create_simple_item(model: Type, val: str):
    item, _ = db.get_or_create(
        model,
        lookup={"title": val}
    )

    return item


def set_team_season_data(team: Team, team_season_data: pd.DataFrame):
    for _, single_team_season_data in team_season_data.iterrows():
        team_season = TeamSeason(
            games=single_team_season_data['Games (G)'],
            wins=single_team_season_data['Wins (W)'],
            losses=single_team_season_data['Losses (L)'],
            minutes_played=single_team_season_data['Minutes Played (MP)'],
            pace_factor=single_team_season_data['Pace Factor (Pace)'],
            relative_pace=single_team_season_data['Relative Pace'],
            offensive_rating=single_team_season_data['Offensive Rating (ORtg)'],
            relative_offensive_rating=single_team_season_data['Relative Offensive Rating'],
            defensive_rating=single_team_season_data['Defensive Rating (DRtg)'],
            relative_defensive_rating=single_team_season_data['Relative Defensive Rating'],
            points=single_team_season_data['Points (PTS)'],
            opponent_points_per_game=single_team_season_data[
                'Opponent Points Per Game (Opp Pts/G)'],
            three_point_field_goals_made=single_team_season_data[
                '3-Point Field Goals Made (3P)'],
            three_point_field_goals_attempts=single_team_season_data[
                '3-Point Field Goal Attempts (3PA)'],
            two_point_field_goals_made=single_team_season_data[
                '2-Point Field Goals Made (2P)'],
            two_point_field_goals_attempts=single_team_season_data[
                '2-Point Field Goal Attempts (2PA)'],
            free_throws_made=single_team_season_data['Free Throws Made (FT)'],
            free_throws_attempts=single_team_season_data['Free Throw Attempts (FTA)'],
            ft_per_fga=single_team_season_data['FT/FGA'],
            offensive_rebounds=single_team_season_data['Offensive Rebounds (ORB)'],
            offensive_rebound_percentage=single_team_season_data[
                'Offensive Rebound Percentage (ORB%)'],
            defensive_rebounds=single_team_season_data['Defensive Rebounds (DRB)'],
            defensive_rebound_percentage=single_team_season_data[
                'Defensive Rebound Percentage (DRB%)'],
            total_rebounds=single_team_season_data['Total Rebounds (TRB)'],
            total_rebound_percentage=single_team_season_data[
                'Total Rebound Percentage (TRB%)'],
            assists=single_team_season_data['Assists (AST)'],
            assist_percentage=single_team_season_data['Assist Percentage (AST%)'],
            steals=single_team_season_data['Steals (STL)'],
            steal_percentage=single_team_season_data['Steal Percentage (STL%)'],
            blocks=single_team_season_data['Blocks (BLK)'],
            block_percentage=single_team_season_data['Block Percentage (BLK%)'],
            turnovers=single_team_season_data['Turnovers (TOV)'],
            turnover_percentage=single_team_season_data['Turnover Percentage (TOV%)'],
            personal_fouls=single_team_season_data['Personal Fouls (PF)'],
            standing=single_team_season_data['Standing'],
            conference_standing=single_team_season_data['Conference Standing'],
            conference_champion=single_team_season_data['Conference Champion'],
            champion=single_team_season_data['Champion'],
            season=get_or_create_simple_item(
                Season, single_team_season_data['Season']
            ),
            arena=get_or_create_simple_item(
                Arena, single_team_season_data['Arena']
            ),
            playoff_result=get_or_create_simple_item(
                PlayoffResult, single_team_season_data['Playoff result']
            )
        )

        team.team_seasons.append(team_season)


def get_season(unvalid_season: str):
    parts = unvalid_season.split('-')

    return parts[0][:2]+parts[1]


def parse_and_set_positions(player: Player, val: str):
    if '"' in val or 'and' in val:
        val = val.replace('"', '')
        pattern = r',\s*and\s|\s*,\s*|\s+and\s*'
        for item in re.split(pattern, val):
            position, _ = db.get_or_create(
                Position,
                lookup={"title": item},
                defaults={"short_title": ''.join(
                    [word[0] for word in item.split()])}
            )

            player_position = PlayerPosition(
                player=player,
                position=position
            )

            player.player_positions.append(player_position)
    else:
        position, _ = db.get_or_create(
            Position,
            lookup={"title": val},
            defaults={"short_title": ''.join(
                [word[0] for word in val.split()])}
        )

        player_position = PlayerPosition(
            player=player,
            position=position
        )

        player.player_positions.append(player_position)


def create_draft(val):
    draft = Draft(
        year=val['Draft Year'],
        round=val['Draft Round'],
        pick=val['Draft Pick'],
        team=db.find_first(Team, name=val['Draft Team'])
    )

    return draft


def set_player_season_data(player: Player, player_season_data: pd.DataFrame):
    for _, single_player_season_data in player_season_data.iterrows():
        player_season = PlayerSeason(
            games_played=single_player_season_data['Games Played (G)'],
            games_started=single_player_season_data['Games Started (GS)'],
            minutes_played=single_player_season_data['Minutes Played (MP)'],
            three_point_field_goals_made=single_player_season_data[
                '3-Point Field Goals Made (3P)'],
            three_point_field_goals_attempts=single_player_season_data[
                '3-Point Field Goal Attempts (3PA)'],
            two_point_field_goals_made=single_player_season_data[
                '2-Point Field Goals Made (2P)'],
            two_point_field_goals_attempts=single_player_season_data[
                '2-Point Field Goal Attempts (2PA)'],
            effective_field_goals_percentage=single_player_season_data[
                'Effective Field Goal Percentage (eFG%)'],
            free_throws_made=single_player_season_data['Free Throws Made (FT)'],
            free_throws_attempts=single_player_season_data['Free Throw Attempts (FTA)'],
            offensive_rebounds=single_player_season_data['Offensive Rebounds (ORB)'],
            offensive_rebound_percentage=single_player_season_data[
                'Offensive Rebound Percentage (ORB%)'],
            defensive_rebounds=single_player_season_data['Defensive Rebounds (DRB)'],
            defensive_rebound_percentage=single_player_season_data[
                'Defensive Rebound Percentage (DRB%)'],
            total_rebounds=single_player_season_data['Total Rebounds (TRB)'],
            total_rebound_percentage=single_player_season_data[
                'Total Rebound Percentage (TRB%)'],
            assists=single_player_season_data['Assists (AST)'],
            assist_percentage=single_player_season_data['Assist Percentage (AST%)'],
            steals=single_player_season_data['Steals (STL)'],
            steal_percentage=single_player_season_data['Steal Percentage (STL%)'],
            blocks=single_player_season_data['Blocks (BLK)'],
            block_percentage=single_player_season_data['Block Percentage (BLK%)'],
            turnovers=single_player_season_data['Turnovers (TOV)'],
            turnover_percentage=single_player_season_data['Turnover Percentage (TOV%)'],
            personal_fouls=single_player_season_data['Personal Fouls (PF)'],
            points=single_player_season_data['Points (PTS)'],
            player_efficiency_rating=single_player_season_data[
                'Player Efficiency Rating (PER)'],
            position=db.get_or_create(
                Position,
                lookup={"short_title": single_player_season_data['Position']}
            )[0],
            team_season=get_team_season(
                single_player_season_data['Team'], single_player_season_data['Season'])
        )

        player.player_seasons.append(player_season)


def get_team_season(team_short_name: str, season: str):
    team_season = db.session.query(TeamSeason).join(Team).join(Season).filter(
        Season.title == season,
        Team.short_name == team_short_name
    ).first()

    return team_season


def get_award(id: int):
    award, _ = db.get_or_create(
        Award,
        lookup={"id": id}
    )

    return award


def get_player_season(season: str, player_name: str):
    player_season = db.session.query(PlayerSeason)\
        .join(Player, Player.id == PlayerSeason.player_id)\
        .join(TeamSeason, TeamSeason.id == PlayerSeason.team_season_id)\
        .join(Season, Season.id == TeamSeason.season_id)\
        .filter(
            Season.title == season,
            Player.name == player_name
        ).first()
        
    print(player_season)

    return player_season


file_path = "basketball_reference.db"

if os.path.exists(file_path):
    os.remove(file_path)

with Database() as db:
    for csv_file in Path("./data/raw").glob("*.csv"):
        file_name = csv_file.stem  # file name without format
        globals()[file_name] = pd.read_csv(csv_file)

    for _, team_item in teams_data.iterrows():
        team = Team(
            name=team_item['Name'],
            short_name=team_item['Short Name'],
            franchise=team_item['Franchise'],
            _from=team_item['From'],
            to=team_item['To'],
            playoff_appearances=team_item['Playoff Appearances (Plyfs)'],
            championships=team_item['Championships'],

            conference=get_or_create_simple_item(
                Conference, team_item['Conference']
            ),
            division=get_or_create_simple_item(
                Division, team_item['Division']
            )
        )

        set_team_season_data(
            team,
            team_season_data[team_season_data['Team Name'] == team.name]
        )

        db.add(team)
        db.commit()

    for _, award_item in awards.iterrows():
        award = Award(
            id=award_item['ID'],
            short_name=award_item['Award Short Name'],
            trophy_name=award_item['Trophy Name'],
            description=award_item['Description'],
        )

        db.add(award)
        db.commit()

    for _, player_item in players_data.iterrows():
        player = Player(
            name=player_item['Name'],
            _from=get_season(player_item['From']),
            to=get_season(player_item['To']),
            height=player_item['Height'],
            weight=player_item['Weight'],
            birth_date=datetime.strptime(
                str(player_item['Birth Date']), "%Y-%m-%d") if not pd.isna(player_item['Birth Date']) else None,
            experience=player_item['Experience'],
            shoots=0 if player_item['Shoots'] == 'Right' else 1,
            nationality=get_or_create_simple_item(
                Nationality, player_item['Nationality']
            ),
            college=get_or_create_simple_item(
                College, player_item['College']
            ),
            draft=create_draft(player_item[[
                'Draft Year',
                'Draft Round',
                'Draft Pick',
                'Draft Team'
            ]])
        )

        parse_and_set_positions(player, player_item['Position'])

        set_player_season_data(
            player,
            player_season_data[player_season_data['Player Name']
                               == player.name]
        )

        db.add(player)
        db.commit()

    for _, award_season_item in award_season_data.iterrows():
        player_season_award = PlayerSeasonAward(
            award=get_award(award_season_item['Award ID']),
            player_season=get_player_season(get_season(award_season_item['Season']), award_season_item['Player Name'])
        )

        db.add(player_season_award)
        db.commit()
