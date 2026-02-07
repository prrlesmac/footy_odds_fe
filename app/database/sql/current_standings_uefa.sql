create OR REPLACE VIEW public.current_standings_uefa AS
WITH matches AS (
    SELECT
        home AS team,
        country AS league,
        CASE 
            WHEN home_goals > away_goals THEN 3
            WHEN home_goals = away_goals THEN 1
            WHEN home_goals < away_goals THEN 0
        ELSE NULL
        END AS pts
    FROM public.fixtures_uefa
    WHERE played='Y' 
        AND round='League'

    UNION ALL

    SELECT
        away AS team,
        country AS league,
        CASE 
            WHEN home_goals > away_goals THEN 0
            WHEN home_goals = away_goals THEN 1
            WHEN home_goals < away_goals THEN 3
        ELSE NULL
        END AS pts
    FROM public.fixtures_uefa
    WHERE played='Y' 
        AND round='League'
)
SELECT 
    team,
    league,
    SUM(pts) AS pts
FROM matches
GROUP BY team, league;
