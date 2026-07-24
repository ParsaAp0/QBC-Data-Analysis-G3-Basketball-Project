import pandas as pd

from database import get_connection
from utils import *


def load_players():

    print("Loading Players...")

    df = pd.read_csv("data/final/players_data.csv")

    conn = get_connection()

    cursor = conn.cursor()

    sql = """
    INSERT IGNORE INTO Players
    (
        player_id,
        name,
        birth_date,
        height,
        weight,
        nationality,
        position,
        shoots,
        college,
        draft_year,
        draft_round,
        draft_pick,
        draft_team
    )

    VALUES
    (
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
    )
    """

    inserted = 0

    for _, row in df.iterrows():

        values = (

            clean(row["ID"]),

            clean(row["Name"]),

            parse_date(row["Birth Date"]),

            height(row["Height"]),

            weight_to_kg(row["Weight"]),

            clean(row["Nationality"]),

            clean(row["Position"]),

            clean(row["Shoots"]),

            clean(row["College"]),

            clean(row["Draft Year"]),

            clean(row["Draft Round"]),

            clean(row["Draft Pick"]),

            clean(row["Draft Team"])

        )

        try:

            cursor.execute(sql, values)

            inserted += 1

        except Exception as e:
            
            print("Player Error :", row["Name"])

            print(e)

            

    conn.commit()

    cursor.close()

    conn.close()

    print(f"{inserted} Players Inserted")