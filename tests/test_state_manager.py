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

def test_filter_new_plays_ignore_time_change(state_manager):
    # Already seen Play A on "08 lut 18:00"
    # The key should be normalized to "Play A|08 lut"
    state_manager.save_seen_plays({"Play A|08 lut"})
    
    scraped_plays = [
        {"title": "Play A", "date": "08 lut 19:00"}, # Different time, same date
    ]
    
    new_plays = state_manager.filter_new_plays(scraped_plays)
    
    # Should be ignored because the date (08 lut) is the same
    assert len(new_plays) == 0

def test_filter_new_plays_keep_time_in_notification(state_manager):
    # Nothing seen yet
    scraped_plays = [
        {"title": "Play B", "date": "10 mar 20:00"},
    ]
    
    new_plays = state_manager.filter_new_plays(scraped_plays)
    
    assert len(new_plays) == 1
    # Should still have the time in the date string for notification
    assert new_plays[0]['date'] == "10 mar 20:00"