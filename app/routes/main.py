from flask import Blueprint, render_template, redirect, url_for
from app.models.league import LeagueService

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Main page with summary table of odds for all leagues."""
    footy_league_data = LeagueService.get_all_footy_league_data()
    nfl_data = LeagueService.get_all_nfl_data()
    nba_data = LeagueService.get_all_nba_data()
    return render_template('landing_page.html',
                           footy_league_data=footy_league_data,
                           nfl_data=nfl_data,
                           nba_data=nba_data)

@main_bp.route('/league')
def league_default():
    """Default league view - redirects to first available league."""
    leagues = LeagueService.get_league_names()
    
    if not leagues:
        return "No leagues available", 404
    
    first_league = leagues[0]
    return redirect(url_for('main.league_detail', league_name=first_league))


@main_bp.route('/league/<league_name>')
def league_detail(league_name):
    """Detailed view for a specific league."""
    league_data = LeagueService.get_all_footy_league_data()
    
    if league_name not in league_data:
        return "League not found", 404
    
    standings = league_data[league_name]["standings"]
    fixtures = league_data[league_name]["fixtures"]
    leagues = LeagueService.get_league_names()
    updated_at = standings[0].get('updated_at') if standings else None
    
    return render_template(
        'league_odds.html',
        standings=standings,
        fixtures=fixtures,
        leagues=leagues,
        selected_league=league_name,
        updated_at=updated_at
    )

@main_bp.route('/NFL')
def league_detail_nfl():
    """Detailed view for a specific league."""
    league_data = LeagueService.get_all_nfl_data()

    if "NFL" not in league_data:
        return "League not found", 404
    
    standings = league_data["NFL"]["standings"]
    fixtures = league_data["NFL"]["fixtures"]
    leagues = LeagueService.get_league_names()
    updated_at = standings[0].get('updated_at') if standings else None

    return render_template(
        'nfl_odds.html',
        standings=standings,
        fixtures=fixtures,
        leagues=leagues,
        selected_league="NFL",
        updated_at=updated_at
    )

@main_bp.route('/NBA')
def league_detail_nba():
    """Detailed view for a specific league."""
    league_data = LeagueService.get_all_nba_data()

    if "NBA" not in league_data:
        return "League not found", 404
    
    standings = league_data["NBA"]["standings"]
    fixtures = league_data["NBA"]["fixtures"]
    leagues = LeagueService.get_league_names()
    updated_at = standings[0].get('updated_at') if standings else None

    return render_template(
        'nba_odds.html',
        standings=standings,
        fixtures=fixtures,
        leagues=leagues,
        selected_league="NBA",
        updated_at=updated_at
    )

@main_bp.route('/about')
def about_website():
    """About view. Gives info about the website"""
    return render_template('about.html')
