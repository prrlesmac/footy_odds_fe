import pytest
from app import create_app

@pytest.fixture(scope="module")
def test_client():
    app = create_app()
    with app.test_client() as client:
        yield client

def test_index(test_client):
    resp = test_client.get("/")
    assert resp.status_code == 200

def test_league_default(test_client):
    resp = test_client.get("/league")
    # Accept 200 or redirect (302) if no leagues
    assert resp.status_code in (200, 302)

def test_about(test_client):
    resp = test_client.get("/about")
    assert resp.status_code == 200

def test_health(test_client):
    resp = test_client.get("/health")
    assert resp.status_code == 200

def test_nfl(test_client):
    resp = test_client.get("/NFL")
    assert resp.status_code in (200, 404)

def test_nba(test_client):
    resp = test_client.get("/NBA")
    assert resp.status_code in (200, 404)

def test_mlb(test_client):
    resp = test_client.get("/MLB")
    assert resp.status_code in (200, 404)

# def test_fifa_wc(test_client):
#     resp = test_client.get("/FIFA_WC")
#     assert resp.status_code in (200, 404)

# Dynamic league detail test (uses first league if available)
def test_league_detail(test_client):
    resp = test_client.get("/league")
    if resp.status_code == 302 and "Location" in resp.headers:
        # Follow redirect to actual league
        league_url = resp.headers["Location"]
        league_resp = test_client.get(league_url)
        assert league_resp.status_code == 200
    elif resp.status_code == 200:
        assert True  # Page loaded
    else:
        assert False, f"Unexpected status: {resp.status_code}"
