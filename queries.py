from sqlalchemy import text

get_domestic_league_data = text(f"""
    SELECT 
        team,
        elo,
        champion,
        top_4,
        relegation_playoff,
        relegation_direct,
        league,
        s.updated_at
    FROM public.sim_standings_dom s 
    LEFT JOIN public.current_elos c 
    ON s.team = c.club
    ORDER by
        league,
        champion DESC,
        top_4 DESC,
        relegation_direct ASC,
        elo DESC
    """
)

get_continental_league_data = text(f"""
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
            s.updated_at
        FROM public.sim_standings_con s 
        LEFT JOIN public.current_elos c 
        ON s.team = c.club
        ORDER by
            league,
            po_champion DESC,
            po_r2 DESC,
            po_r4 DESC,
            po_r8 DESC,
            po_r16 DESC,
            po_r32 DESC,
            elo DESC
        """
)