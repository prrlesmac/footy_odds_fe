LEAGUE_MAPPING = {
  #  'UCL': 'UEFA Champions League',
  #  'UEL': 'UEFA Europa League', 
  #  'UECL': 'UEFA Conference League',
    'ENG': 'Premier League (England)',
    'ESP': 'La Liga (Spain)',
    'ITA': 'Serie A (Italy)',
    'GER': 'Bundesliga (Germany)',
    'FRA': 'Ligue 1 (France)'
}

# Reverse mapping for convenience
LEAGUE_REVERSE_MAPPING = {v: k for k, v in LEAGUE_MAPPING.items()}

# Ordered list for consistent display
LEAGUE_ORDER = list(LEAGUE_MAPPING.values())