import json

games = []

def load_games():
    try:
        with open('games.json', "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_games():
    with open('games.json', "w") as file:
        json.dump(games, file)

games = load_games()

def display_menu():
    print("===================================")
    print("      Game Management System       ")
    print("===================================")
    print("1. Add Game")
    print("2. Edit Game Details")
    print("3. Update Play Status")
    print("4. Delete Game Entry")
    print("5. View All Games")
    print("6. View Games by Platform")
    print("7. View Games by Status")
    print("8. View Game Ratings")
    print("9. Exit")
    print("===================================")

def add_game():
    title = input("Enter Game Title: ").strip()
    platform = input("Enter Platform (PC, PS5, Switch): ").strip()
    play_status = input("Enter Play Status (Unplayed, Playing, Completed, Abandoned): ").strip()
    hours_played = float(input("Enter Hours Played: "))
    rating = int(input("Enter Rating (1-10): "))

    game = {
        'title': title,
        'platform': platform,
        'play_status': play_status,
        'hours_played': hours_played,
        'rating': rating,
    }

    games.append(game)
    save_games()
    print(f"Game '{title}' added successfully.")

def edit_game():
    title = input("Enter the title of the game to edit: ").strip()
    for game in games:
        if title.lower() == game['title'].lower():
            game['platform'] = input("Enter new Platform: ").strip()
            game['play_status'] = input("Enter new Play Status: ").strip()
            game['hours_played'] = float(input("Enter new Hours Played: "))
            game['rating'] = int(input("Enter new Rating (1-10): "))
            save_games()
            print(f"Details updated for '{title}'.")
            return
    print(f"No game found with title '{title}'.")

def update_play_status():
    title = input("Enter the title of the game to update status: ").strip()
    for game in games:
        if title.lower() == game['title'].lower():
            new_status = input("Enter new Play Status (Unplayed, Playing, Completed, Abandoned): ").strip()
            game['play_status'] = new_status
            save_games()
            print(f"Play status updated to '{new_status}' for game '{title}'.")
            return
    print(f"No game found with title '{title}'.")

def delete_game():
    title = input("Enter the title of the game to delete: ").strip()
    for game in games:
        if title.lower() == game['title'].lower():
            games.remove(game)
            save_games()
            print(f"Game '{title}' deleted successfully.")
            return
    print(f"No game found with title '{title}'.")

def view_all_games():
    if not games:
        print("No games to display.")
        return
    for game in games:
        print(f"Title: {game['title']}")
        print(f"Platform: {game['platform']}")
        print(f"Status: {game['play_status']}")
        print(f"Hours Played: {game['hours_played']}")
        print(f"Rating: {game['rating']}/10")
        print("---------------------------------------")

def view_by_platform():
    platform = input("Enter platform to filter by: ").strip()
    filtered = [g for g in games if g['platform'].lower() == platform.lower()]
    if not filtered:
        print(f"No games found for platform '{platform}'.")
        return
    for game in filtered:
        print(f"- {game['title']} ({game['play_status']}, {game['hours_played']} hrs, {game['rating']}/10)")

def view_by_status():
    status = input("Enter status to filter by (Unplayed, Playing, Completed, Abandoned): ").strip()
    filtered = [g for g in games if g['play_status'] == status]
    if not filtered:
        print(f"No games found with status '{status}'.")
        return
    for game in filtered:
        print(f"- {game['title']} on {game['platform']} ({game['hours_played']} hrs)")

def view_ratings():
    if not games:
        print("No games to display.")
        return
    sorted_games = sorted(games, key=lambda g: g['rating'], reverse=True)
    print("Game Ratings:")
    for game in sorted_games:
        print(f"{game['title']} - {game['rating']}/10")

def main():
    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()
        print("===================================")

        if choice == '1':
            add_game()
        elif choice == '2':
            edit_game()
        elif choice == '3':
            update_play_status()
        elif choice == '4':
            delete_game()
        elif choice == '5':
            view_all_games()
        elif choice == '6':
            view_by_platform()
        elif choice == '7':
            view_by_status()
        elif choice == '8':
            view_ratings()
        elif choice == '9':
            save_games()
            print("Goodbye, gamer!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()