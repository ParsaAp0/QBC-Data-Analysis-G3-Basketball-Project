import pandas as pd

from database import get_connection
from utils import clean
from loaders.lookups import get_team_lookup


def load_team_seasons():

    print("-------------------------------")
    print("Loading Team Season Stats ...")
    print("-------------------------------")

    df = pd.read_csv("basketball_ETL/CSVs/team_season_data.csv")

    team_lookup = get_team_lookup()

    conn = get_connection()

    cursor = conn.cursor()

    sql = """
    INSERT IGNORE INTO TeamSeasonStats
    (
        team_id,
        season,
        wins,
        losses,
        standing,
        conference_standing,
        playoff_result,
        conference_champion,
        champion
    )

    VALUES
    (
        %s,%s,%s,%s,%s,%s,%s,%s,%s
    )
    """

    inserted = 0
    skipped = 0

    for _, row in df.iterrows():

        team_name = str(row["Team Name"]).strip().lower()

        team_id = team_lookup.get(team_name)

        if team_id is None:

            print(f"Team Not Found : {team_name}")

            skipped += 1

            continue

        values = (

            team_id,

            clean(row["Season"]),

            clean(row["Wins (W)"]),

            clean(row["Losses (L)"]),

            clean(row["Standing"]),

            clean(row["Conference Standing"]),

            clean(row["Playoff result"]),

            clean(row["Conference Champion"]),

            clean(row["Champion"])

        )

        try:

            cursor.execute(sql, values)

            inserted += 1

        except Exception as e:

            print(team_name)
            print(e)
            skipped += 1

    conn.commit()

    cursor.close()

    conn.close()

    print(f"Inserted : {inserted}")
    print(f"Skipped  : {skipped}")