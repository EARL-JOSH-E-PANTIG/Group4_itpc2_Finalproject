import requests

BASE_URL = "http://localhost:5000/api/"

def display_menu():
    print("\n" + "=" * 50)
    print("GAME MANAGEMENT SYSTEM".center(50))
    print("=" * 50)
    print("1. List All Games")
    print("2. View Game Details")
    print("3. Add New Game")
    print("4. Update Game")
    print("5. Delete Game")
    print("6. Exit")
    print("=" * 50)


def list_games():
    try:
        response = requests.get(f"{BASE_URL}/games")
        if response.status_code == 200:
            games = response.json()
            if not games:
                print("\nNo games found.")
                return
            print("\n" + "-" * 80)
            print(f"{'Title':<20}{'Platform':<15}{'Status':<15}{'Hours':<10}{'Rating':<10}")
            print("-" * 80)
            for g in games:
                print(f"{g['title']:<20}{g['platform']:<15}{g['play_status']:<15}{g['hours_played']:<10}{g['rating']}/10")
            print("-" * 80)
        else:
            print(f"\nError: {response.text}")
    except requests.RequestException as e:
        print(f"\nConnection error: {e}")


def view_game():
    title = input("Enter game title: ").strip()
    try:
        response = requests.get(f"{BASE_URL}/games/{title}")
        if response.status_code == 200:
            game = response.json()
            print("\n" + "-" * 50)
            print("GAME DETAILS".center(50))
            print("-" * 50)
            print(f"Title       : {game['title']}")
            print(f"Platform    : {game['platform']}")
            print(f"Status      : {game['play_status']}")
            print(f"Hours Played: {game['hours_played']}")
            print(f"Rating      : {game['rating']}/10")
            print("-" * 50)
        elif response.status_code == 404:
            print("Game not found.")
        else:
            print(f"Error: {response.text}")
    except requests.RequestException as e:
        print(f"Connection error: {e}")


def add_game():
    print("\nEnter game details:")
    title = input("Title: ").strip()
    platform = input("Platform (PC, PS5, Switch): ").strip()
    status = input("Play Status (Unplayed, Playing, Completed, Abandoned): ").strip().capitalize()
    try:
        hours = float(input("Hours Played: "))
        rating = int(input("Rating (1-10): "))
    except ValueError:
        print("Invalid number entered.")
        return

    game = {
        "title": title,
        "platform": platform,
        "play_status": status,
        "hours_played": hours,
        "rating": rating
    }

    try:
        response = requests.post(f"{BASE_URL}/games", json=game)
        if response.status_code == 201:
            print("Game added successfully!")
        else:
            print(f"Error adding game: {response.text}")
    except requests.RequestException as e:
        print(f"Connection error: {e}")


def update_game():
    title = input("Enter the title of the game to update: ").strip()
    try:
        get_response = requests.get(f"{BASE_URL}/games/{title}")
        if get_response.status_code != 200:
            print("Game not found.")
            return
        game = get_response.json()
        print(f"Current platform    : {game['platform']}")
        print(f"Current play status : {game['play_status']}")
        print(f"Current hours played: {game['hours_played']}")
        print(f"Current rating      : {game['rating']}")

        new_platform = input("New platform (leave blank to keep current): ").strip()
        new_status = input("New play status (leave blank to keep current): ").strip().capitalize()
        new_hours = input("New hours played (leave blank to keep current): ").strip()
        new_rating = input("New rating (leave blank to keep current): ").strip()

        updates = {}
        if new_platform: updates['platform'] = new_platform
        if new_status: updates['play_status'] = new_status
        if new_hours:
            try: updates['hours_played'] = float(new_hours)
            except ValueError: print("Invalid hours value."); return
        if new_rating:
            try: updates['rating'] = int(new_rating)
            except ValueError: print("Invalid rating value."); return

        if not updates:
            print("No changes made.")
            return

        put_response = requests.put(f"{BASE_URL}/games/{title}", json=updates)
        if put_response.status_code == 200:
            print("Game updated successfully.")
        else:
            print(f"Error updating game: {put_response.text}")
    except requests.RequestException as e:
        print(f"Connection error: {e}")


def delete_game():
    title = input("Enter the title of the game to delete: ").strip()
    confirm = input(f"Are you sure you want to delete '{title}'? (y/n): ")
    if confirm.lower() != 'y':
        print("Deletion cancelled.")
        return
    try:
        response = requests.delete(f"{BASE_URL}/games/{title}")
        if response.status_code == 200:
            print("Game deleted successfully.")
        else:
            print(f"Error deleting game: {response.text}")
    except requests.RequestException as e:
        print(f"Connection error: {e}")


def main():
    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ").strip()
        if choice == '1':
            list_games()
        elif choice == '2':
            view_game()
        elif choice == '3':
            add_game()
        elif choice == '4':
            update_game()
        elif choice == '5':
            delete_game()
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()