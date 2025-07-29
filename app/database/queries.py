from sqlalchemy import text

class LeagueQueries:
    """SQL queries for league data."""
    
    @staticmethod
    def get_domestic_league_data():
        return text("""
            WITH CTE AS (
                SELECT 
                team,
                elo,
                champion,
                top_4,
                relegation_playoff,
                relegation_direct,
                league,
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
                LEFT JOIN public.current_elos c 
                ON s.team = c.club                  
            )
            SELECT 
                team,
                elo,
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
                team,
                elo,
                po_r32,
                po_r16,
                po_r8,  
                po_r4,
                po_r2,
                po_champion,
                league,
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
                LEFT JOIN public.current_elos c 
                ON s.team = c.club                            
            )
            SELECT 
                team,
                elo,
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