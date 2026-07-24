import pandas as pd

from database import get_connection
from utils import *


def load_awards():

    print("Loading Awards...")

    df = pd.read_csv("data/final/awards.csv")

    conn = get_connection()

    cursor = conn.cursor()

    sql = """
    INSERT IGNORE INTO Awards
    (
        award_id,
        short_name,
        trophy_name,
        description
    )

    VALUES
    (
        %s,%s,%s,%s
    )
    """

    inserted = 0

    for _, row in df.iterrows():

        values = (

            clean(row["ID"]),

            clean(row["Award Short Name"]),

            clean(row["Trophy Name"]),

            clean(row["Description"])

        )

        try:

            cursor.execute(sql, values)

            inserted += 1

        except Exception as e:

            print(row["Award Short Name"])

            print(e)

    conn.commit()

    cursor.close()

    conn.close()

    print(f"{inserted} Awards Inserted")