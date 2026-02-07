import os
import json
import pytest
from src.state_manager import StateManager

@pytest.fixture
def temp_state_file(tmp_path):
    return tmp_path / "test_seen_plays.json"

@pytest.fixture
def state_manager(temp_state_file):
    return StateManager(state_file=str(temp_state_file))

def test_get_seen_plays_empty(state_manager):
    assert state_manager.get_seen_plays() == set()

def test_save_and_get_seen_plays(state_manager):
    keys = {"Play 1|Date 1", "Play 2|Date 2"}
    state_manager.save_seen_plays(keys)
    assert state_manager.get_seen_plays() == keys

def test_filter_new_plays_new_date(state_manager):
    # Already seen Play A on Date 1
    state_manager.save_seen_plays({"Play A|Date 1"})
    
    scraped_plays = [
        {"title": "Play A", "date": "Date 1"}, # Old
        {"title": "Play A", "date": "Date 2"}, # New date!
    ]
    
    new_plays = state_manager.filter_new_plays(scraped_plays)
    
    assert len(new_plays) == 1
    assert new_plays[0]['title'] == "Play A"
    assert new_plays[0]['date'] == "Date 2"