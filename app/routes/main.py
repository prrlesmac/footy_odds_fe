from flask import Blueprint, render_template
from app.models.league import LeagueService

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Main page with summary table of odds for all leagues."""
    league_data = LeagueService.get_all_league_data()
    return render_template('landing_page.html', league_data=league_data)

@main_bp.route('/league/<league_name>')
def league_detail(league_name):
    """Detailed view for a specific league."""
    league_data = LeagueService.get_all_league_data()
    
    if league_name not in league_data:
        return "League not found", 404
    
    data = league_data[league_name]
    leagues = LeagueService.get_league_names()
    updated_at = data[0].get('updated_at') if data else None
    
    return render_template(
        'league_odds.html',
        data=data,
        leagues=leagues,
        selected_league=league_name,
        updated_at=updated_at
    )