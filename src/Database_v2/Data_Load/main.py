from loaders.load_players import load_players
from loaders.load_teams import load_teams
from loaders.load_awards import load_awards
from loaders.load_team_seasons import load_team_seasons
from loaders.load_player_seasons import load_player_seasons
from loaders.load_award_seasons import load_award_seasons


def main():

    print("\n----- ETL Started -----\n")

    load_players()

    load_teams()

    load_awards()

    load_team_seasons()

    load_player_seasons()

    load_award_seasons()

    print("\n----- ETL Finished Successfully -----\n")


if __name__ == "__main__":
    main()