try:
    from .scraper import TheaterScraper
    from .state_manager import StateManager
    from .notifier import EmailNotifier
except ImportError:
    from scraper import TheaterScraper
    from state_manager import StateManager
    from notifier import EmailNotifier
import os

def run_checker():
    print("Starting Theater Checker...")
    
    scraper = TheaterScraper()
    state_manager = StateManager()
    notifier = EmailNotifier()

    # 1. Scrape upcoming plays
    print("Fetching upcoming plays...")
    all_plays = scraper.get_upcoming_plays()
    if not all_plays:
        print("No plays found or error during scraping.")
        return

    # 2. Filter for new ones
    new_plays = state_manager.filter_new_plays(all_plays)
    
    if not new_plays:
        print("No new plays found.")
        return

    print(f"Found {len(new_plays)} new plays!")

    # 3. Enrich new plays with descriptions (if not already fetched)
    for play in new_plays:
        if not play.get('description') or play['description'] == "No description available.":
            print(f"Fetching description for: {play['title']}...")
            play['description'] = scraper.get_play_description(play['url'])

    # 4. Notify
    if notifier.send_notification(new_plays):
        # 5. Update state only if notification was successful (or in mock mode)
        seen_keys = state_manager.get_seen_plays()
        for play in new_plays:
            seen_keys.add(state_manager._get_key(play))
        state_manager.save_seen_plays(seen_keys)
        print("State updated and notification sent.")
    else:
        print("Failed to send notification. State not updated.")

if __name__ == "__main__":
    run_checker()
