 create or replace view public.current_standings_nba as  
    WITH matches AS (
        SELECT
            home AS team,
            CASE 
                WHEN home_goals > away_goals THEN 1
                WHEN home_goals <= away_goals THEN 0
            ELSE NULL
            END AS wins,
            CASE 
                WHEN home_goals < away_goals THEN 1
                WHEN home_goals >= away_goals THEN 0
            ELSE NULL
            END AS losses,
            CASE 
                WHEN home_goals = away_goals THEN 1
                WHEN home_goals <> away_goals THEN 0
            ELSE NULL
            END AS ties
        FROM public.fixtures_nba
        WHERE played='Y' 

        UNION ALL

        SELECT
            away AS team,
            CASE 
                WHEN home_goals < away_goals THEN 1
                WHEN home_goals >= away_goals THEN 0
            ELSE NULL
            END AS wins,
            CASE 
                WHEN home_goals > away_goals THEN 1
                WHEN home_goals <= away_goals THEN 0
            ELSE NULL
            END AS losses,
            CASE 
                WHEN home_goals = away_goals THEN 1
                WHEN home_goals <> away_goals THEN 0
            ELSE NULL
            END AS ties
        FROM public.fixtures_nba
        WHERE played='Y'  
    )
    SELECT 
        team,
        SUM(wins) AS wins,
        SUM(losses) AS losses,
        SUM(ties) AS ties
    FROM matches
    GROUP BY team;