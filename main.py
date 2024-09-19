import mysql.connector
import requests

def connect_to_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='vr_games',
        charset='utf8mb4',  # Setze den Zeichensatz
        collation='utf8mb4_general_ci'  # Setze die Kollation
    )

def get_reviews(appid):
    url = f"https://store.steampowered.com/appreviews/{appid}?json=1&language=all&purchase_type=all"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['query_summary']['total_reviews']
    else:
        return None
    
def list_games():
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("SELECT vr_games.name, vr_games.steam_reviews")
    games = cursor.fetchall()
    for game in games:
        print(f"Name: {game[0]}, Steam_Reviews: {game[1]}")
    cursor.close()
    connection.close()

def add_game():
    connection = connect_to_db()
    cursor = connection.cursor()
    sql = "INSERT INTO vr_games (name, steam_id) VALUES (%s, %s)"
    # TODO Get number of reviews
    steam_reviews = 0
    cursor.execute(sql, (name, steam_id, steam_reviews))
    connection.commit()
    cursor.close()
    connection.close()
    print("Game added successfully!")
    
def main():
    while True:
        print("\nWelcome to VRGameMeter")
        print("1. List games")
        print("2. Add game")
        print("3. Update games")
        print("4: Get number of Steam reviews for game")
        print("5: Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            list_games()
        elif choice == '2':
            name = input("Name of game: ")
            steam_id = input("Steam ID: ")
            add_game(name, steam_id)
        elif choice == '3':
            break #TODO
        elif choice == '4':
            app_id = input("App ID of game:")
            steam_reviews = get_reviews(app_id)
            print(f"The game has {steam_reviews} total reviews.")
        elif choice == '5':
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == '__main__':
    main()
    