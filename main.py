import mysql.connector
import requests

def connect_to_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='vr_games',
        charset='utf8mb4',
        collation='utf8mb4_general_ci'
    )

def get_reviews(appid):
    url = f"https://store.steampowered.com/appreviews/{appid}?json=1&language=all&purchase_type=all"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['query_summary']['total_reviews']
    else:
        return None
    
def get_name(appid):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()[f'{appid}']['data']['name']
    else:
        return None
    
def list_games():
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("SELECT name, steam_reviews from vr_games order by steam_reviews desc")
    games = cursor.fetchall()
    for game in games:
        print(f"Name: {game[0]}, Steam_Reviews: {game[1]}")
    cursor.close()
    connection.close()

def add_game(steam_id, vr_only):
    connection = connect_to_db()
    cursor = connection.cursor()
    steam_reviews = get_reviews(steam_id)
    name = get_name(steam_id)
    cursor.execute(f"INSERT INTO vr_games (name, steam_id, steam_reviews, vr_only) VALUES (\"{name}\", {steam_id}, {steam_reviews}, {vr_only}) on duplicate key update steam_reviews = {steam_reviews}")
    connection.commit()
    cursor.close()
    connection.close()
    print("Game added successfully!")

def update():
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("SELECT steam_id from vr_games")
    steam_ids = cursor.fetchall()
    for (steam_id,) in steam_ids:
        steam_reviews = get_reviews(steam_id)
        cursor.execute("UPDATE vr_games SET steam_reviews = %s WHERE steam_id = %s", (steam_reviews, steam_id));
    connection.commit()
    cursor.close()
    connection.close()
    print("Games updated successfully!")
    
def main():
    print("\nWelcome to VRGameMeter")
    print("1. List games")
    print("2. Add game")
    print("3. Update games")
    print("4: Get number of Steam reviews for game")
    print("5: Get title of game")
    choice = input("Choose an option: ")

######################### List games ################################
    if choice == '1':
        list_games()

######################### Add game ##################################
    elif choice == '2':
        steam_id = input("Steam ID: ")
        vr_only = input("VR Only: ")
        vr_only = True if vr_only == '1' else False
        add_game(steam_id, vr_only)

######################### Update games ##############################
    elif choice == '3':
        update()

######################### Get number of reviews #####################
    elif choice == '4':
        steam_id = input("Steam ID:")
        steam_reviews = get_reviews(steam_id)
        print(f"The game has {steam_reviews} total reviews.")

######################### Get name of game #########################
    elif choice == '5':
        steam_id = input("Steam ID:")
        name = get_name(steam_id)
        print(f"The name of the game is {name}.")

######################### Exit ######################################
    else:
        return 0

if __name__ == '__main__':
    main()
    