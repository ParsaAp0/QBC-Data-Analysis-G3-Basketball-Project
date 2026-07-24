import pandas as pd

from database import get_connection
from utils import clean
from loaders.lookups import get_team_lookup

def load_team_seasons():

    print("-------------------------------")
    print("Loading Team Season Stats ...")
    print("-------------------------------")

    df = pd.read_csv("data/final/team_season_data.csv")

    team_lookup = get_team_lookup()

    conn = get_connection()

    cursor = conn.cursor()

    sql = """
    INSERT IGNORE INTO TeamSeasonStats
    (
        `team_id`,
        `season`,
        `wins`,
        `losses`,
        `standing`,
        `conference_standing`,
        `playoff_result`,
        `conference_champion`,
        `champion`,
        `games`,
        `W/L%`,
        `MP`,
        `pace`,
        `relative_pace`,
        `ORtg`,
        `relative_ORtg`,
        `DRtg`,
        `relative_DRtg`,
        `Pts/G`,
        `Opp Pts/G`,
        `fg`,
        `fga`,
        `fg%`,
        `3p`,
        `3pa`,
        `3p%`,
        `2p`,
        `2pa`,
        `2p%`,
        `eFG%`,
        `ft`,
        `fta`,
        `ft%`,
        `ft/fga`,
        `orb`,
        `orb%`,
        `drb`,
        `drb%`,
        `trb`,
        `trb/G`,
        `ast`,
        `ast/G`,
        `stl`,
        `stl/G`,
        `blk`,
        `blk/G`,
        `tov`,
        `tov/G`,
        `fouls`,
        `fouls/G`
    )

    VALUES
    (
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s
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

            clean(row["Champion"]),

            clean(row["Games (G)"]),
            
            clean(row["Win/Loss Percentage (W/L%)"]),

            clean(row["Minutes Played (MP)"]),

            clean(row["Pace Factor (Pace)"]),

            clean(row["Relative Pace"]),

            clean(row["Offensive Rating (ORtg)"]),

            clean(row["Relative Offensive Rating"]),

            clean(row["Defensive Rating (DRtg)"]),

            clean(row["Relative Defensive Rating"]),

            clean(row["Points Per Game (Pts/G)"]),

            clean(row["Opponent Points Per Game (Opp Pts/G)"]),

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
            
            clean(row["FT/FGA"]),
            
            clean(row["Offensive Rebounds (ORB)"]),
            
            clean(row["Offensive Rebound Percentage (ORB%)"]),
            
            clean(row["Defensive Rebounds (DRB)"]),
            
            clean(row["Defensive Rebound Percentage (DRB%)"]),
            
            clean(row["Total Rebounds (TRB)"]),
            
            clean(row["Total Rebounds Per Game"]),
            
            clean(row["Assists (AST)"]),
            
            clean(row["Assists Per Game"]),
            
            clean(row["Steals (STL)"]),
            
            clean(row["Steals Per Game"]),
            
            clean(row["Blocks (BLK)"]),
            
            clean(row["Blocks Per Game"]),
            
            clean(row["Turnovers (TOV)"]),
            
            clean(row["Turnovers Per Game"]),
            
            clean(row["Personal Fouls (PF)"]),
            
            clean(row["Personal Fouls Per Game"])
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