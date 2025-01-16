from flask import Blueprint, jsonify, request
from models import Player, db

player_bp = Blueprint('players', __name__)

@player_bp.route("/api/players", methods=["GET", "POST"])
def manage_players():
    if request.method == "POST":
        data = request.json
        new_player = Player(
            name=data["name"],
            level=data["level"],
            ac=data["ac"],
            initiative_modifier=data["initiativeModifier"]
        )
        db.session.add(new_player)
        db.session.commit()
        return jsonify({
            "id": new_player.id,
            "name": new_player.name,
            "level": new_player.level,
            "ac": new_player.ac,
            "initiativeModifier": new_player.initiative_modifier
        }), 201

    players = Player.query.all()
    return jsonify([
        {
            "id": player.id,
            "name": player.name,
            "level": player.level,
            "ac": player.ac,
            "initiativeModifier": player.initiative_modifier
        } for player in players
    ])
def get_parties():
    parties = Party.query.all()
    return jsonify([{"id": p.id, "name": p.name} for p in parties])

@player_bp.route("/api/players/<int:player_id>", methods=["PUT", "DELETE"])
def modify_player(player_id):
    player = Player.query.get(player_id)
    if not player:
        return jsonify({"error": "Player not found"}), 404

    if request.method == "PUT":
        data = request.json
        player.name = data.get("name", player.name)
        player.level = data.get("level", player.level)
        player.ac = data.get("ac", player.ac)
        player.initiative_modifier = data.get("initiativeModifier", player.initiative_modifier)
        db.session.commit()
        return jsonify({
            "id": player.id,
            "name": player.name,
            "level": player.level,
            "ac": player.ac,
            "initiativeModifier": player.initiative_modifier
        })

    if request.method == "DELETE":
        db.session.delete(player)
        db.session.commit()
        return jsonify({"message": "Player deleted"})


