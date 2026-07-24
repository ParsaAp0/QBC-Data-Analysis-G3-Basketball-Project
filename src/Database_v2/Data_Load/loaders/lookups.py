from database import get_connection


def get_player_lookup():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT player_id, name
        FROM Players
""")

    players = {}

    for player_id, name in cursor.fetchall():
        players[name.strip().lower()] = player_id

    cursor.close()
    conn.close()

    return players


TEAM_ABBR_OVERRIDE = {
    "brk": "NJN",   # Brooklyn Nets -> short_name is NJN in teams_data
    "cho": "CHA",   # Charlotte Hornets -> short_name is CHA in teams_data
    "nop": "NOH",   # New Orleans Pelicans -> short_name is NOH in teams_data
}


def get_team_lookup():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT team_id, name, short_name
        FROM Teams
    """)

    teams = {}

    for team_id, name, short_name in cursor.fetchall():
        # Map full name (lowered)
        teams[name.strip().lower()] = team_id
        # Map short_name (lowered)
        if short_name:
            teams[short_name.strip().lower()] = team_id

    cursor.close()
    conn.close()

    # Add abbreviation overrides where CSV uses different codes than teams_data.csv
    for abbr, override_abbr in TEAM_ABBR_OVERRIDE.items():
        if override_abbr.lower() in teams:
            teams[abbr] = teams[override_abbr.lower()]

    return teams