import json
import os
import re

class StateManager:
    def __init__(self, state_file="seen_plays.json"):
        self.state_file = state_file

    def _extract_date_only(self, date_str):
        """Removes time part from date string (e.g. '08 lut 18:00' -> '08 lut')."""
        return re.sub(r'\s+\d{1,2}:\d{2}$', '', date_str)

    def _get_keys(self, play):
        """Generates a list of unique keys for each date of a play (excluding time)."""
        title = play['title']
        dates = play['date'].split(", ")
        return [f"{title}|{self._extract_date_only(d)}" for d in dates]

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
                            # Normalize key by stripping time
                            normalized_d = self._extract_date_only(d)
                            seen.add(f"{title}|{normalized_d}")
                    else:
                        # Fallback for unexpected format (normalize just in case)
                        seen.add(self._extract_date_only(item))
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
        Normalization is done to ignore time changes for the same date.
        If a play has some new dates and some old dates, only new dates are returned.
        """
        seen_keys = self.get_seen_plays()
        new_plays = []

        for p in plays:
            original_dates = p['date'].split(", ")
            new_dates_with_time = []

            for d in original_dates:
                # Normalize key by stripping time to check if we've seen this title+date before
                normalized_key = f"{p['title']}|{self._extract_date_only(d)}"
                if normalized_key not in seen_keys:
                    new_dates_with_time.append(d)

            if new_dates_with_time:
                # Create a copy with only the new dates (keeping their original format with time)
                new_play = p.copy()
                new_play['date'] = ", ".join(new_dates_with_time)
                new_plays.append(new_play)

        return new_plays