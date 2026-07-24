import pandas as pd
from database import get_connection
from utils import clean
from loaders.lookups import get_player_lookup


def load_award_seasons():

    print("-------------------------------")
    print("Loading Award Seasons ...")
    print("-------------------------------")

    df = pd.read_csv("data/final/award_season_data.csv")

    player_lookup = get_player_lookup()

    conn = get_connection()

    cursor = conn.cursor()

    sql = """
    INSERT IGNORE INTO AwardSeason
    (
        award_id,
        player_id,
        season
    )

    VALUES
    (
        %s,%s,%s
    )
    """

    inserted = 0
    skipped = 0

    for _, row in df.iterrows():

        player_name = str(row["Player Name"]).strip().lower()
        player_id = player_lookup.get(player_name)

        if player_id is None:
            skipped += 1
            continue

        values = (

            clean(row["Award ID"]),

            player_id,

            clean(row["Season"])

        )

        try:

            cursor.execute(sql, values)

            inserted += 1

        except Exception as e:

            print(f"{player_name}: {e}")
            skipped += 1

    conn.commit()

    cursor.close()

    conn.close()

    print(f"Inserted : {inserted}")
    print(f"Skipped  : {skipped}")