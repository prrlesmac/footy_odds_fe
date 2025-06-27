from flask import Flask, render_template, request
import pandas as pd
import db
import config

app = Flask(__name__)

def get_football_data(league):
    engine = db.get_postgres_engine()
    query = f"""
    SELECT 
        team,
        elo,
        title_odds,
        top_4_odds,
        {'relegation_playoff_odds,' if league in ['GER','FRA'] else ''}
        direct_relegation_odds
    FROM public.sim_standings s 
    LEFT JOIN public.current_elos c 
    ON s.team = c.club
    WHERE s.country='{league}'
    """
    standings = pd.read_sql(query, engine)
    return standings

@app.route('/')
def index():
    leagues = list(config.league_mapping.keys())
    selected_league = request.args.get('league', leagues[0])
    df = get_football_data(config.league_mapping[selected_league])
    data=df.to_dict(orient='records')
    return render_template(
        'table.html',
        data=df.to_dict(orient='records'),
        leagues=leagues,
        selected_league=selected_league
    )

if __name__ == '__main__':
    app.run(debug=True, port=8050)
