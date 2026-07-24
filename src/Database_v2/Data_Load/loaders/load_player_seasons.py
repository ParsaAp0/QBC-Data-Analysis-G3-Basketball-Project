import pandas as pd
from database import get_connection
from utils import clean
from loaders.lookups import get_player_lookup, get_team_lookup


# multi-team entries in CSV — skip these rows
SKIP_TEAM_ABBRS = {"2tm", "3tm", "4tm"}

def get_experience_lookup():

    df = pd.read_csv("data/CSVs/players_data.csv")

    lookup = {}

    for _, row in df.iterrows():

        lookup[str(row["Name"]).strip().lower()] = clean(row["Experience"])

    return lookup


def load_player_seasons():

    print("-------------------------------")
    print("Loading Player Season Stats ...")
    print("-------------------------------")

    df = pd.read_csv("data/CSVs/player_season_data.csv")

    player_lookup = get_player_lookup()

    team_lookup = get_team_lookup()

    experience_lookup = get_experience_lookup()

    conn = get_connection()

    cursor = conn.cursor()

    sql = """
    INSERT IGNORE INTO PlayerSeasonStats
    (
        player_id,
        team_id,
        season,
        position,
        experience,
        games,
        games_started,
        minutes,
        fg,
        fga,
        fg_percent,
        three_p,
        three_pa,
        three_percent,
        two_p,
        two_pa,
        two_percent,
        efg,
        ft,
        fta,
        ft_percent,
        orb,
        drb,
        trb,
        ast,
        stl,
        blk,
        tov,
        pf,
        pts,
        per
    )

    VALUES
    (
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
    )
    """

    inserted = 0

    skipped = 0

    for _, row in df.iterrows():

        player_name = str(row["Player Name"]).strip().lower()

        team_abbr = str(row["Team"]).strip().lower()

        # Skip multi-team entries (traded mid-season)
        if team_abbr in SKIP_TEAM_ABBRS:
            skipped += 1
            continue

        player_id = player_lookup.get(player_name)

        team_id = team_lookup.get(team_abbr)

        experience = experience_lookup.get(player_name)

        if player_id is None:

            print("--------------------------------")
            print("PLAYER NOT FOUND")
            print("CSV :", repr(row["Player Name"]))
            print("KEY :", repr(player_name))
            print("--------------------------------")

            skipped += 1
            continue

        if team_id is None:

            print("--------------------------------")
            print("TEAM NOT FOUND")
            print("CSV :", repr(row["Team"]))
            print("KEY :", repr(team_abbr))
            print("--------------------------------")

            skipped += 1
            continue

        values = (

            player_id,

            team_id,

            clean(row["Season"]),

            clean(row["Position"]),

            experience,

            clean(row["Games Played (G)"]),

            clean(row["Games Started (GS)"]),

            clean(row["Minutes Played (MP)"]),

            clean(row["Field Goals Made (FG)"]),

            clean(row["Field Goal Attempts (FGA)"]),

            clean(row["Field Goal Percentage (FG%)"]),

            clean(row["3-Point Field Goals Made (3P)"]),

            clean(row["3-Point Field Goal Attempts (3PA)"]),

            clean(row["3-Point Field Goal Percentage (3P%)"]),

            clean(row["2-Point Field Goals Made (2P)"]),

            clean(row["2-Point Field Goal Attempts (2PA)"]),

            clean(row["2-Point Field Goal Percentage (2P%)"]),

            clean(row["Effective Field Goal Percentage (eFG%)"]),

            clean(row["Free Throws Made (FT)"]),

            clean(row["Free Throw Attempts (FTA)"]),

            clean(row["Free Throw Percentage (FT%)"]),

            clean(row["Offensive Rebounds (ORB)"]),

            clean(row["Defensive Rebounds (DRB)"]),

            clean(row["Total Rebounds (TRB)"]),

            clean(row["Assists (AST)"]),

            clean(row["Steals (STL)"]),

            clean(row["Blocks (BLK)"]),

            clean(row["Turnovers (TOV)"]),

            clean(row["Personal Fouls (PF)"]),

            clean(row["Points (PTS)"]),

            clean(row["Player Efficiency Rating (PER)"])

        )

        try:

            cursor.execute(sql, values)

            inserted += 1

        except Exception as e:

            print("----------------------------------")
            print(player_name)
            print(e)
            print("----------------------------------")

            skipped += 1

    conn.commit()

    cursor.close()

    conn.close()

    print()

    print(f"Inserted : {inserted}")

    print(f"Skipped  : {skipped}")

    print()