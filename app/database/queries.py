from sqlalchemy import text

class LeagueQueries:
    """SQL queries for league data."""
    
    @staticmethod
    def get_domestic_league_data():
        return text("""
            WITH CTE AS (
                SELECT 
                s.team,
                elo,
                pts,
                champion,
                top_4,
                relegation_playoff,
                relegation_direct,
                s.league,
                s.updated_at,
                CASE WHEN champion <= 0.015
                THEN 0
                ELSE champion
                END AS champion_floor,
                CASE WHEN top_4 <= 0.015
                THEN 0
                ELSE top_4
                END AS top_4_floor,
                CASE WHEN relegation_direct <= 0.015
                THEN 0
                ELSE relegation_direct
                END AS relegation_direct_floor
                FROM public.sim_standings_dom s 
                LEFT JOIN public.current_standings_uefa cs 
                ON s.team = cs.team    
                    AND s.league = cs.league  
                LEFT JOIN public.current_elos_uefa c 
                ON s.team = c.club                  
            )
            SELECT 
                team,
                elo,
                pts,
                champion,
                top_4,
                relegation_playoff,
                relegation_direct,
                league,
                updated_at
            FROM CTE
            ORDER by
                league,
                champion_floor DESC,
                top_4_floor DESC,
                relegation_direct_floor ASC,
                elo DESC
        """)
    
    @staticmethod
    def get_continental_league_data():
        return text("""
            WITH CTE AS (
                SELECT 
                s.team,
                elo,
                pts,
                direct_to_round_of_16,
                po_r32,
                po_r16,
                po_r8,  
                po_r4,
                po_r2,
                po_champion,
                s.league,
                s.updated_at,
                CASE WHEN po_champion <= 0.015
                THEN 0
                ELSE po_champion
                END AS po_champion_floor,
                CASE WHEN po_r2 <= 0.015
                THEN 0
                ELSE po_r2
                END AS po_r2_floor,
                CASE WHEN po_r4 <= 0.015
                THEN 0
                ELSE po_r4
                END AS po_r4_floor,
                CASE WHEN po_r8 <= 0.015
                THEN 0
                ELSE po_r8
                END AS po_r8_floor,
                CASE WHEN po_r16 <= 0.015
                THEN 0
                ELSE po_r16
                END AS po_r16_floor,
                CASE WHEN po_r32 <= 0.015
                THEN 0
                ELSE po_r32
                END AS po_r32_floor
                FROM public.sim_standings_con s 
                LEFT JOIN public.current_standings_uefa cs 
                ON s.team = cs.team  
                    AND s.league = cs.league
                LEFT JOIN public.current_elos_uefa c 
                ON s.team = c.club                            
            )
            SELECT 
                team,
                elo,
                pts,
                direct_to_round_of_16,
                po_r32,
                po_r16,
                po_r8,  
                po_r4,
                po_r2,
                po_champion AS champion,
                league,
                updated_at
            FROM CTE
            ORDER by
                league,
                po_champion_floor DESC,
                po_r2_floor DESC,
                po_r4_floor DESC,
                po_r8_floor DESC,
                po_r16_floor DESC,
                po_r32_floor DESC,
                elo DESC
        """)
    
    @staticmethod
    def get_fixtures_data(table_name):
        return text(f"""
            SELECT
                home,
                away,
                date,
                country
            FROM public.{table_name}
            WHERE played='N'
            ORDER BY DATE   
        """)
    
    @staticmethod
    def get_nfl_league_data():
         return text("""
            WITH CTE AS (
                SELECT
                s.team,
                division,
                wins || '-' || losses || 
                CASE WHEN ties > 0 
                     THEN '-' || ties
                     ELSE ''
                     END
                AS record,
                elo,
                first_round_bye,
                po_r16,
                po_r8,  
                po_r4,
                po_r2,
                po_champion,
                s.updated_at,
                CASE WHEN po_champion <= 0.015
                THEN 0
                ELSE po_champion
                END AS po_champion_floor,
                CASE WHEN po_r2 <= 0.015
                THEN 0
                ELSE po_r2
                END AS po_r2_floor,
                CASE WHEN po_r4 <= 0.015
                THEN 0
                ELSE po_r4
                END AS po_r4_floor,
                CASE WHEN po_r8 <= 0.015
                THEN 0
                ELSE po_r8
                END AS po_r8_floor,
                CASE WHEN po_r16 <= 0.015
                THEN 0
                ELSE po_r16
                END AS po_r16_floor
                FROM public.sim_standings_nfl s 
                LEFT JOIN public.current_standings_nfl cs 
                ON s.team = cs.team  
                LEFT JOIN public.current_elos_nfl c 
                ON s.team = c.club        
                LEFT JOIN public.teams_nfl t
                ON s.team = t.team               
            )
            SELECT 
                team,
                division,
                record,
                elo,
                first_round_bye,
                po_r16,
                po_r8,  
                po_r4,
                po_r2,
                po_champion AS champion,
                'NFL' AS league,
                updated_at
            FROM CTE
            ORDER by
                league,
                po_champion_floor DESC,
                po_r2_floor DESC,
                po_r4_floor DESC,
                po_r8_floor DESC,
                po_r16_floor DESC,
                elo DESC
        """)
    
    @staticmethod
    def get_nba_league_data():
         return text("""
            WITH CTE AS (
                SELECT
                s.team,
                conference,
                wins || '-' || losses || 
                CASE WHEN ties > 0 
                     THEN '-' || ties
                     ELSE ''
                     END
                AS record,
                elo,
                po_r16,
                po_r8,  
                po_r4,
                po_r2,
                po_champion,
                s.updated_at,
                CASE WHEN po_champion <= 0.015
                THEN 0
                ELSE po_champion
                END AS po_champion_floor,
                CASE WHEN po_r2 <= 0.015
                THEN 0
                ELSE po_r2
                END AS po_r2_floor,
                CASE WHEN po_r4 <= 0.015
                THEN 0
                ELSE po_r4
                END AS po_r4_floor,
                CASE WHEN po_r8 <= 0.015
                THEN 0
                ELSE po_r8
                END AS po_r8_floor,
                CASE WHEN po_r16 <= 0.015
                THEN 0
                ELSE po_r16
                END AS po_r16_floor
                FROM public.sim_standings_nba s 
                LEFT JOIN public.current_standings_nba cs 
                ON s.team = cs.team  
                LEFT JOIN public.current_elos_nba c 
                ON s.team = c.club        
                LEFT JOIN public.teams_nba t
                ON s.team = t.team               
            )
            SELECT 
                team,
                conference,
                record,
                elo,
                po_r16,
                po_r8,  
                po_r4,
                po_r2,
                po_champion AS champion,
                'NBA' AS league,
                updated_at
            FROM CTE
            ORDER by
                league,
                po_champion_floor DESC,
                po_r2_floor DESC,
                po_r4_floor DESC,
                po_r8_floor DESC,
                po_r16_floor DESC,
                elo DESC
        """)