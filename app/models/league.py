from collections import defaultdict
from app.database.connection import DatabaseConnection
from app.database.queries import LeagueQueries
from app.config.leagues import UEFA_LEAGUE_MAPPING, UEFA_LEAGUE_ORDER
from app.services.team_mapper import map_team_name

class LeagueService:
    """Service class for league-related operations."""
    
    @staticmethod
    def get_all_footy_league_data():
        """Get organized league data for all leagues."""
        # Fetch data from database
        domestic_data = DatabaseConnection.execute_query(
            LeagueQueries.get_domestic_league_data()
        )
        continental_data = DatabaseConnection.execute_query(
            LeagueQueries.get_continental_league_data()
        )
        # Fetch upcoming matches data
        fixtures_data = DatabaseConnection.execute_query(
            LeagueQueries.get_fixtures_data("fixtures_uefa")
        )
        # Combine and organize data
        all_data = domestic_data + continental_data
        league_dict = defaultdict(lambda: defaultdict(list))
        # Convert to dictionaries and group by league
        for row in all_data:
            row_dict = row._asdict()
            row_dict['team'] = map_team_name(row_dict['team'])
            mapped_league = UEFA_LEAGUE_MAPPING.get(row_dict['league'], row_dict['league'])
            league_dict[mapped_league]["standings"].append(row_dict)

        for row in fixtures_data:
            row_dict = row._asdict()
            row_dict['home'] = map_team_name(row_dict['home'])
            row_dict['away'] = map_team_name(row_dict['away'])
            mapped_league = UEFA_LEAGUE_MAPPING.get(row_dict['country'], row_dict['country'])
            league_dict[mapped_league]["fixtures"].append(row_dict)
        
        # Sort according to predefined order
        ordered_dict = {
            league: league_dict[league] 
            for league in UEFA_LEAGUE_ORDER 
            if league in league_dict
        }

        return ordered_dict

    @staticmethod
    def get_all_nfl_data():
        """Get organized league data for all leagues."""
        nfl_data = DatabaseConnection.execute_query(
            LeagueQueries.get_nfl_league_data()
        )
        # Fetch upcoming matches data
        fixtures_data = DatabaseConnection.execute_query(
            LeagueQueries.get_fixtures_data("fixtures_nfl")
        )
        league_dict = defaultdict(lambda: defaultdict(list))

        # Convert to dictionaries and group by league
        for row in nfl_data:
            row_dict = row._asdict()
            league_dict["NFL"]["standings"].append(row_dict)

        for row in fixtures_data:
            row_dict = row._asdict()
            league_dict["NFL"]["fixtures"].append(row_dict)
        
        return league_dict

    @staticmethod
    def get_all_nba_data():
        """Get organized league data for all leagues."""
        nba_data = DatabaseConnection.execute_query(
            LeagueQueries.get_nba_league_data()
        )
        # Fetch upcoming matches data
        fixtures_data = DatabaseConnection.execute_query(
            LeagueQueries.get_fixtures_data("fixtures_nba")
        )
        league_dict = defaultdict(lambda: defaultdict(list))

        # Convert to dictionaries and group by league
        for row in nba_data:
            row_dict = row._asdict()
            league_dict["NBA"]["standings"].append(row_dict)

        for row in fixtures_data:
            row_dict = row._asdict()
            league_dict["NBA"]["fixtures"].append(row_dict)
        
        return league_dict
    
    @staticmethod
    def get_all_mlb_data():
        """Get organized league data for all leagues."""
        mlb_data = DatabaseConnection.execute_query(
            LeagueQueries.get_mlb_league_data()
        )
        # Fetch upcoming matches data
        fixtures_data = DatabaseConnection.execute_query(
            LeagueQueries.get_fixtures_data("fixtures_mlb")
        )
        league_dict = defaultdict(lambda: defaultdict(list))

        # Convert to dictionaries and group by league
        for row in mlb_data:
            row_dict = row._asdict()
            league_dict["MLB"]["standings"].append(row_dict)

        for row in fixtures_data:
            row_dict = row._asdict()
            league_dict["MLB"]["fixtures"].append(row_dict)
        
        return league_dict

    @staticmethod
    def get_league_names():
        """Get list of all league names."""
        from app.config.leagues import UEFA_LEAGUE_REVERSE_MAPPING
        return list(UEFA_LEAGUE_REVERSE_MAPPING.keys())