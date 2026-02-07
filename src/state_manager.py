import json
import os

class StateManager:
    def __init__(self, state_file="seen_plays.json"):
        self.state_file = state_file

    def _get_key(self, play):
        """Generates a unique key for a play based on title and dates."""
        return f"{play['title']}|{play['date']}"

    def get_seen_plays(self):
        """Loads the list of seen play keys from the state file."""
        if not os.path.exists(self.state_file):
            return set()
        
        try:
            with open(self.state_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return set(data)
        except (json.JSONDecodeError, IOError):
            return set()

    def save_seen_plays(self, seen_keys):
        """Saves the list of seen play keys to the state file."""
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(list(seen_keys), f, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"Error saving state to {self.state_file}: {e}")

    def filter_new_plays(self, plays):
        """
        Filters a list of plays to return only those that haven't been seen before.
        A play is considered new if its combination of title and dates is new.
        """
        seen_keys = self.get_seen_plays()
        new_plays = [p for p in plays if self._get_key(p) not in seen_keys]
        return new_plays