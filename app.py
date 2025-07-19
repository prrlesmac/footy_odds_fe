from flask import Flask, render_template, request
import pandas as pd
import db
import queries
import config
from collections import defaultdict

app = Flask(__name__)
engine = db.get_postgres_engine()


def get_league_data(league_mapping):
    domestic_league_data = db.get_sql_data(engine, queries.get_domestic_league_data)
    continental_league_data = db.get_sql_data(engine, queries.get_continental_league_data)
    league_data = domestic_league_data + continental_league_data
    league_dict = defaultdict(list)
    dict_list = [row._asdict() for row in league_data]
    for item in dict_list:
        league_dict[league_mapping[item['league']]].append(item)

    order_list = list(league_mapping.values())
    # Sort dictionary keys by their position in the external list
    league_dict = {k: league_dict[k] for k in order_list if k in league_dict}

    return league_dict

@app.route('/')
#have main page with summary table of odds for all leagues
def index():
    league_data = get_league_data(config.league_mapping)
    return render_template(
        'landing_page.html',
        league_data=league_data
    )

@app.route('/league/<league_name>')
def league_detail(league_name):
    league_data = get_league_data(config.league_mapping)
    data = league_data[league_name]
    mapping = {v: k for k, v in config.league_mapping.items()}
    leagues = list(mapping.keys())
    #breakpoint()
    return render_template(
        'league_odds.html',
        data=data,
        leagues=leagues,
        selected_league=league_name,
        updated_at=data[0]['updated_at'] if 'updated_at' in data[0] else None,
    )
if __name__ == '__main__':
    app.run(debug=True, port=8050)
