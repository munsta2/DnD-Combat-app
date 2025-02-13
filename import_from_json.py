import json
import requests

# Replace with your actual PythonAnywhere API URL
API_URL = "https://trogdor22.pythonanywhere.com/api/monsters"

def push_monsters_to_database(json_file):
    """
    Reads a JSON file containing monster data and sends it to the database.
    
    Args:
        json_file (str): Path to the JSON file.
    """
    try:
        # Load the JSON data
        with open(json_file, "r") as file:
            monsters = json.load(file)

        if not isinstance(monsters, list):
            raise ValueError("JSON file must contain an array of monsters.")

        for monster in monsters:
            response = requests.post(API_URL, json=monster)

            # Check the response from the server
            if response.status_code == 201:
                print(f"Successfully added monster: {monster['name']}")
            else:
                print(f"Failed to add monster: {monster['name']}")
                print(f"Response {response.status_code}: {response.text}")

    except FileNotFoundError:
        print(f"Error: File '{json_file}' not found.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON file format.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Path to your JSON file
json_file_path = "monster.json"

# Push monsters to the database
push_monsters_to_database(json_file_path)
