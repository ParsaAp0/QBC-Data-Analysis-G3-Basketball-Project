import pandas as pd

from database import get_connection
from utils import *


def load_teams():

    print("Loading Teams...")

    df = pd.read_csv("data/final/teams_data.csv")

    conn = get_connection()

    cursor = conn.cursor()

    sql = """
    INSERT IGNORE INTO Teams
    (
        team_id,
        name,
        franchise,
        conference,
        division,
        short_name
    )

    VALUES
    (
        %s,%s,%s,%s,%s,%s
    )
    """

    inserted = 0

    for _, row in df.iterrows():

        values = (

            clean(row["ID"]),

            clean(row["Name"]),

            clean(row["Franchise"]),

            clean(row["Conference"]),

            clean(row["Division"]),

            clean(row["Short Name"])

        )

        try:

            cursor.execute(sql, values)

            inserted += 1

        except Exception as e:

            print(row["Name"])

            print(e)

    conn.commit()

    cursor.close()

    conn.close()

    print(f"{inserted} Teams Inserted")