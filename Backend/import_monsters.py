import json
from models import db, Monster
from app import app

def parse_monster_data(json_monster):
    """
    Map the JSON monster data to the Monster model.
    """
    def parse_int(value, default=0):
        try:
            return int(value)
        except (ValueError, TypeError):
            return default

    def parse_float(value, default=0.0):
        try:
            return float(value.split()[0]) if isinstance(value, str) else float(value)
        except (ValueError, TypeError):
            return default

    return Monster(
        name=json_monster.get("name", ""),
        size=json_monster.get("meta", "").split()[0],
        type=json_monster.get("meta", "").split(",")[0].split()[-1],
        alignment=json_monster.get("meta", "").split(",")[-1].strip() if "," in json_monster.get("meta", "") else "",
        hp=parse_int(json_monster.get("Hit Points", "0").split()[0]),
        ac=parse_int(json_monster.get("Armor Class", "0").split()[0]),
        speed=json_monster.get("Speed", "").strip(),
        str=parse_int(json_monster.get("STR", 0)),
        dex=parse_int(json_monster.get("DEX", 0)),
        con=parse_int(json_monster.get("CON", 0)),
        int=parse_int(json_monster.get("INT", 0)),
        wis=parse_int(json_monster.get("WIS", 0)),
        cha=parse_int(json_monster.get("CHA", 0)),
        languages=json_monster.get("Languages", ""),
        damage_vulnerabilities=json_monster.get("Damage Vulnerabilities", ""),
        senses=json_monster.get("Senses", ""),
        challenge_rating=parse_float(json_monster.get("Challenge", "0")),
        actions=json_monster.get("Actions", ""),
        legendary_actions=json_monster.get("Legendary Actions", ""),
        traits=json_monster.get("Traits", ""),
        reactions=json_monster.get("Reactions", ""),
    )

def import_monsters(json_file):
    """
    Import monsters from a JSON file into the database, replacing existing monsters if they have the same name.
    """
    with open(json_file, "r") as file:
        monsters_data = json.load(file)
    
    with app.app_context():
        for json_monster in monsters_data:
            try:
                # Check if the monster already exists in the database
                existing_monster = Monster.query.filter_by(name=json_monster.get("name", "")).first()
                
                if existing_monster:
                    print(f"Replacing existing monster: {existing_monster.name}")
                    db.session.delete(existing_monster)  # Delete the existing monster
                
                # Add the new monster
                monster = parse_monster_data(json_monster)
                db.session.add(monster)
            
            except Exception as e:
                print(f"Error processing monster {json_monster.get('name', 'Unknown')}: {e}")
        
        db.session.commit()
        print(f"Imported {len(monsters_data)} monsters successfully.")

if __name__ == "__main__":
    # Replace with the path to your JSON file
    json_file_path = "srd_5e_monsters.json"
    import_monsters(json_file_path)
