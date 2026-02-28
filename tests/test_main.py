import pytest
from unittest.mock import patch, MagicMock
from src.main import run_checker

def test_run_checker_new_plays_found():
    # Mock dependencies
    with patch('src.main.TheaterScraper') as MockScraper, \
         patch('src.main.StateManager') as MockStateManager, \
         patch('src.main.EmailNotifier') as MockNotifier:
        
        scraper_inst = MockScraper.return_value
        state_inst = MockStateManager.return_value
        notifier_inst = MockNotifier.return_value
        
        # Setup mock behavior
        scraper_inst.get_upcoming_plays.return_value = [
            {"title": "New Play", "date": "Date", "url": "http://url"}
        ]
        state_inst.filter_new_plays.return_value = [
            {"title": "New Play", "date": "Date", "url": "http://url"}
        ]
        state_inst._get_keys.return_value = ["New Play|Date"]
        notifier_inst.send_notification.return_value = True
        state_inst.get_seen_plays.return_value = set()
        
        # Run orchestrator
        run_checker()
        
        # Verify interactions
        scraper_inst.get_upcoming_plays.assert_called_once()
        state_inst.filter_new_plays.assert_called_once()
        notifier_inst.send_notification.assert_called_once()
        state_inst.save_seen_plays.assert_called_once()
        # Verify it saved the key, not just the title
        assert state_inst.save_seen_plays.call_args[0][0] == {"New Play|Date"}

def test_run_checker_no_new_plays():
    with patch('src.main.TheaterScraper') as MockScraper, \
         patch('src.main.StateManager') as MockStateManager, \
         patch('src.main.EmailNotifier') as MockNotifier:
        
        scraper_inst = MockScraper.return_value
        state_inst = MockStateManager.return_value
        notifier_inst = MockNotifier.return_value
        
        scraper_inst.get_upcoming_plays.return_value = [{"title": "Old Play"}]
        state_inst.filter_new_plays.return_value = []
        
        run_checker()
        
        notifier_inst.send_notification.assert_not_called()
        state_inst.save_seen_plays.assert_not_called()
