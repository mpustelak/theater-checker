import pytest
from unittest.mock import patch, MagicMock
from src.notifier import EmailNotifier
import os

@pytest.fixture
def notifier():
    with patch.dict(os.environ, {"MOCK_EMAIL": "true", "RECIPIENT_EMAIL": "test@example.com"}):
        return EmailNotifier()

def test_notifier_mock_mode(notifier, capsys):
    new_plays = [
        {"title": "Play A", "date": "Jan 1", "url": "http://link.a", "description": "Desc A"}
    ]
    
    success = notifier.send_notification(new_plays)
    
    assert success is True
    captured = capsys.readouterr()
    assert "--- MOCK EMAIL START ---" in captured.out
    assert "To: test@example.com" in captured.out
    assert "Tytuł: Play A" in captured.out
    assert "Opis: Desc A" in captured.out
    assert "znalazłem dla Ciebie nowe spektakle" in captured.out

def test_notifier_no_plays(notifier, capsys):
    success = notifier.send_notification([])
    assert success is None
    captured = capsys.readouterr()
    assert captured.out == ""

def test_notifier_multiple_recipients(capsys):
    with patch.dict(os.environ, {
        "MOCK_EMAIL": "true", 
        "RECIPIENT_EMAIL": "user1@example.com;user2@example.com"
    }):
        notifier = EmailNotifier()
        notifier.send_notification([{"title": "Test", "date": "Now", "url": "http://test"}])
        
        captured = capsys.readouterr()
        assert "To: user1@example.com, user2@example.com" in captured.out