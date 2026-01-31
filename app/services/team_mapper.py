TEAM_NAME_MAP = {
    "Eintracht Frankfurt": "Eint Frankfurt",
    "Paris Saint-Germain": "Paris S-G",
    "Newcastle United": "Newcastle",
    "Tottenham Hotspur": "Tottenham",
    "Maccabi Tel Aviv FC": "Macc Tel Aviv",
    "Lincoln Red Imps FC": "Lincoln Imps",
    "Ħamrun Spartans FC": "Ħamrun Spartans",
    "Ludogorets Razgrad": "Ludogorets",
    "Nottingham Forest": "Nottm Forest",
    "Slovan Bratislava": "Slovan Bratisl",
    "Shakhtar Donetsk": "Shakhtar",
}

def map_team_name(db_name: str) -> str:
    return TEAM_NAME_MAP.get(db_name, db_name)