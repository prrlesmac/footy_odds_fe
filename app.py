from flask import Flask, render_template, request
import pandas as pd
import db
import config

app = Flask(__name__)

def get_football_data(league):
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
            po_champion
        FROM public.sim_standings_con s 
        LEFT JOIN public.current_elos c 
        ON s.team = c.club
        WHERE s.league='{league}'
        """
    
    else:
        query = f"""
        SELECT 
            team,
            elo,
            champion,
            top_4,
            {'relegation_playoff,' if league in ['GER','FRA'] else ''}
            relegation_direct
        FROM public.sim_standings_dom s 
        LEFT JOIN public.current_elos c 
        ON s.team = c.club
        WHERE s.league='{league}'
        """
    standings = pd.read_sql(query, engine)
    return standings

@app.route('/')
def index():
    leagues = list(config.league_mapping.keys())
    selected_league = request.args.get('league', leagues[0])
    df = get_football_data(config.league_mapping[selected_league])
    return render_template(
        'table.html',
        data=df.to_dict(orient='records'),
        leagues=leagues,
        selected_league=selected_league
    )

if __name__ == '__main__':
    app.run(debug=True, port=8050)
