from flask import Blueprint, jsonify, request
from models import Monster, db

monster_bp = Blueprint('monsters', __name__)

@monster_bp.route("/api/monsters", methods=["GET", "POST"])
def manage_monsters():
    if request.method == "POST":
        try:
            data = request.json
            new_monster = Monster(
                name=data.get("name", ""),
                size=data.get("size", ""),
                type=data.get("type", ""),
                alignment=data.get("alignment", ""),
                hp=data.get("hp", 0),
                ac=data.get("ac", 0),
                speed=data.get("speed", ""),
                str=data.get("stats", {}).get("str", 0),
                dex=data.get("stats", {}).get("dex", 0),
                con=data.get("stats", {}).get("con", 0),
                int=data.get("stats", {}).get("int", 0),
                wis=data.get("stats", {}).get("wis", 0),
                cha=data.get("stats", {}).get("cha", 0),
                languages=data.get("languages", ""),
                damage_vulnerabilities=data.get("damageVulnerabilities", ""),
                senses=data.get("senses", ""),
                challenge_rating=data.get("challengeRating", 0.0),
                actions=data.get("actions", ""),
                legendary_actions=data.get("legendaryActions", ""),
                traits=data.get("traits", ""),
                reactions=data.get("reactions", ""),
            )
            db.session.add(new_monster)
            db.session.commit()

            return jsonify(new_monster.to_dict()), 201
        except Exception as e:
            print(f"Error adding monster: {e}")
            return jsonify({"error": str(e)}), 400

    elif request.method == "GET":
        try:
            monsters = Monster.query.all()
            return jsonify([monster.to_dict() for monster in monsters])
        except Exception as e:
            print(f"Error fetching monsters: {e}")
            return jsonify({"error": str(e)}), 500
def get_monsters():
    monsters = Monster.query.all()
    return jsonify([{"id": m.id, "name": m.name} for m in monsters])



@monster_bp.route("/api/monsters/<int:monster_id>", methods=["PUT", "DELETE"])
def modify_monster(monster_id):
    monster = Monster.query.get(monster_id)
    if not monster:
        return jsonify({"error": "Monster not found"}), 404

    if request.method == "PUT":
        data = request.json
        monster.name = data.get("name", monster.name)
        monster.size = data.get("size", monster.size)
        monster.type = data.get("type", monster.type)
        monster.alignment = data.get("alignment", monster.alignment)
        monster.hp = data.get("hp", monster.hp)
        monster.ac = data.get("ac", monster.ac)
        monster.speed = data.get("speed", monster.speed)
        monster.stats = data.get("stats", monster.stats)
        monster.actions = data.get("actions", monster.actions)
        monster.legendary_actions = data.get("legendaryActions", monster.legendary_actions)
        monster.traits = data.get("traits", monster.traits)
        monster.reactions = data.get("reactions", monster.reactions)
        monster.languages = data.get("languages", monster.languages)
        monster.damage_vulnerabilities = data.get("damageVulnerabilities", monster.damage_vulnerabilities)
        monster.senses = data.get("senses", monster.senses)
        monster.challenge_rating = data.get("challengeRating", monster.challenge_rating)
        db.session.commit()
        return jsonify({
            "id": monster.id,
            "name": monster.name,
            "size": monster.size,
            "type": monster.type,
            "alignment": monster.alignment,
            "hp": monster.hp,
            "ac": monster.ac,
            "speed": monster.speed,
            "stats": monster.stats,
            "actions": monster.actions,
            "legendaryActions": monster.legendary_actions,
            "traits": monster.traits,
            "reactions": monster.reactions,
            "languages": monster.languages,
            "damageVulnerabilities": monster.damage_vulnerabilities,
            "senses": monster.senses,
            "challengeRating": monster.challenge_rating,
        })

    if request.method == "DELETE":
        db.session.delete(monster)
        db.session.commit()
        return jsonify({"message": "Monster deleted"})
