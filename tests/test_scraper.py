import pytest
from unittest.mock import MagicMock, patch
from src.scraper import TheaterScraper

@pytest.fixture
def scraper():
    return TheaterScraper()

def test_get_upcoming_plays_success(scraper):
    mock_html = """
    <div class="row list-group-item visible-lg">
        <div class="media-body">
            <div class="event-title">FAUST</div>
            <div>
                Opis Fausta.
                <a class="badge badge-cart" href="/details/faust">Opis</a>
            </div>
        </div>
        <div class="col-xs-5">
            <a class="badge badge-purple">08 lut 18:00</a>
        </div>
    </div>
    """
    with patch.object(TheaterScraper, 'BASE_URL', "http://mock-theater.pl/"):
        with patch('requests.Session.get') as mock_get:
            mock_get.return_value.text = mock_html
            mock_get.return_value.status_code = 200
            
            plays = scraper.get_upcoming_plays()
            
            assert len(plays) == 1
            assert plays[0]['title'] == "FAUST"
            assert "Fausta." in plays[0]['description']
            assert "08 lut 18:00" in plays[0]['date']
            assert plays[0]['url'] == "http://mock-theater.pl/details/faust"

def test_get_play_description_placeholder(scraper):
    desc = scraper.get_play_description("http://mock-theater.pl/play")
    assert "already retrieved" in desc
