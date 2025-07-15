from flask import Flask, render_template, request
import pandas as pd
import db
import config
from collections import defaultdict
from sqlalchemy import text

app = Flask(__name__)

def get_single_league_data(league):
    engine = db.get_postgres_engine()
    if league in ['UCL', 'UEL', 'UECL']:
        query = f"""
        SELECT 
            team,
            elo,
            po_r32,
            po_r16,
            po_r8,  
            po_r4,
            po_r2,
            po_champion,
            s.updated_at
        FROM public.sim_standings_con s 
        LEFT JOIN public.current_elos c 
        ON s.team = c.club
        WHERE s.league='{league}'
        ORDER by
            po_champion DESC,
            po_r2 DESC,
            po_r4 DESC,
            po_r8 DESC,
            po_r16 DESC,
            po_r32 DESC,
            elo DESC
        """
    
    else:
        query = f"""
        SELECT 
            team,
            elo,
            champion,
            top_4,
            {'relegation_playoff,' if league in ['GER','FRA'] else ''}
            relegation_direct,
            s.updated_at
        FROM public.sim_standings_dom s 
        LEFT JOIN public.current_elos c 
        ON s.team = c.club
        WHERE s.league='{league}'
        ORDER by
            champion DESC,
            top_4 DESC,
            relegation_direct ASC,
            elo DESC
        """
    standings = pd.read_sql(query, engine)
    return standings


def get_all_league_data(league_mapping):
    engine = db.get_postgres_engine()
    query = text("""
        SELECT 
            team,
            elo,
            league,
            po_champion AS odds
        FROM public.sim_standings_con s 
        LEFT JOIN public.current_elos c 
        ON s.team = c.club
        WHERE po_champion >= 0.001

        UNION ALL

        SELECT 
            team,
            elo,
            league,
            champion as odds
        FROM public.sim_standings_dom s 
        LEFT JOIN public.current_elos c 
        ON s.team = c.club
        WHERE champion >= 0.001
        ORDER by
            league,
            odds DESC
        """
    )
    with engine.connect() as conn:
        result = conn.execute(query)
        rows = result.fetchall()    # Group by league
    league_dict = defaultdict(list)
    
    for row in rows:
        league_dict[league_mapping[row.league]].append({
            'name': row.team,
            'odds': row.odds
        })
    
    # Convert to expected format
    league_data = [
        {
            'name': league_name,
            'teams': teams
        }
        for league_name, teams in league_dict.items()
    ]    
    
    return league_data

@app.route('/')
#have main page with summary table of odds for all leagues
def index():
    data = get_all_league_data(config.league_mapping)
    return render_template(
        'landing_page.html',
        league_data=data,
    )

@app.route('/league/<league_name>')
def league_detail(league_name):
    mapping = {v: k for k, v in config.league_mapping.items()}
    leagues = list(mapping.keys())
    df = get_single_league_data(mapping[league_name])
    return render_template(
        'league_odds.html',
        data=df.to_dict(orient='records'),
        leagues=leagues,
        selected_league=league_name,
        updated_at=df['updated_at'].max() if 'updated_at' in df.columns else None,
    )
if __name__ == '__main__':
    app.run(debug=True, port=8050)
