from collections import defaultdict
from app.database.connection import DatabaseConnection
from app.database.queries import LeagueQueries
from app.config.leagues import LEAGUE_MAPPING, LEAGUE_ORDER

class LeagueService:
    """Service class for league-related operations."""
    
    @staticmethod
    def get_all_league_data():
        """Get organized league data for all leagues."""
        # Fetch data from database
        domestic_data = DatabaseConnection.execute_query(
            LeagueQueries.get_domestic_league_data()
        )
        continental_data = DatabaseConnection.execute_query(
            LeagueQueries.get_continental_league_data()
        )
        
        # Combine and organize data
        all_data = domestic_data + continental_data
        league_dict = defaultdict(list)
        
        # Convert to dictionaries and group by league
        for row in all_data:
            row_dict = row._asdict()
            mapped_league = LEAGUE_MAPPING.get(row_dict['league'], row_dict['league'])
            league_dict[mapped_league].append(row_dict)
        
        # Sort according to predefined order
        ordered_dict = {
            league: league_dict[league] 
            for league in LEAGUE_ORDER 
            if league in league_dict
        }
        
        return ordered_dict
    
    @staticmethod
    def get_league_names():
        """Get list of all league names."""
        from app.config.leagues import LEAGUE_REVERSE_MAPPING
        return list(LEAGUE_REVERSE_MAPPING.keys())