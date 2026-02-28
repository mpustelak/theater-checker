import json
import os

class StateManager:
    def __init__(self, state_file="seen_plays.json"):
        self.state_file = state_file

    def _get_keys(self, play):
        """Generates a list of unique keys for each date of a play."""
        title = play['title']
        dates = play['date'].split(", ")
        return [f"{title}|{d}" for d in dates]

    def get_seen_plays(self):
        """Loads the list of seen play performance keys from the state file."""
        if not os.path.exists(self.state_file):
            return set()

        try:
            with open(self.state_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                seen = set()
                for item in data:
                    # Migration: if item contains multiple dates (old format), split them
                    if "|" in item:
                        title, dates_str = item.split("|", 1)
                        for d in dates_str.split(", "):
                            seen.add(f"{title}|{d}")
                    else:
                        seen.add(item)
                return seen
        except (json.JSONDecodeError, IOError):
            return set()

    def save_seen_plays(self, seen_keys):
        """Saves the list of seen keys to the state file."""
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                # Save as a sorted list for consistency
                json.dump(sorted(list(seen_keys)), f, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"Error saving state to {self.state_file}: {e}")

    def filter_new_plays(self, plays):
        """
        Filters a list of plays to return only the performances that haven't been seen.
        If a play has some new dates and some old dates, only new dates are returned.
        """
        seen_keys = self.get_seen_plays()
        new_plays = []

        for p in plays:
            all_keys = self._get_keys(p)
            new_keys = [k for k in all_keys if k not in seen_keys]

            if new_keys:
                # Create a copy with only the new dates
                new_dates = [k.split("|", 1)[1] for k in new_keys]
                new_play = p.copy()
                new_play['date'] = ", ".join(new_dates)
                new_plays.append(new_play)

        return new_plays