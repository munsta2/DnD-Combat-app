from flask import Blueprint, jsonify, request
from models import Party, Player, db

party_bp = Blueprint('parties', __name__)

@party_bp.route("/api/parties", methods=["GET", "POST"])
def manage_parties():
    if request.method == "POST":

        data = request.json
        new_party = Party(name=data["name"])
        db.session.add(new_party)
        db.session.flush() 
        for player_id in data.get("playerIds", []):
            player = Player.query.get(player_id)
            if player:
                new_party.players.append(player)
      
        db.session.commit()
        return jsonify({
            "id": new_party.id,
            "name": new_party.name,
            "players": [
                {"id": player.id, "name": player.name, "level": player.level} for player in new_party.players
            ]
        }), 201

    parties = Party.query.all()
    return jsonify([
        {
            "id": party.id,
            "name": party.name,
            "players": [
                {"id": player.id, "name": player.name, "level": player.level} for player in party.players
            ]
        } for party in parties
    ])
def get_parties():
    parties = Party.query.all()
    return jsonify([{"id": p.id, "name": p.name} for p in parties])


@party_bp.route("/api/parties/<int:party_id>", methods=["PUT", "DELETE"])
def modify_party(party_id):
    party = Party.query.get(party_id)
    if not party:
        return jsonify({"error": "Party not found"}), 404

    if request.method == "PUT":
        data = request.json
        party.name = data.get("name", party.name)
        party.players = []  # Clear current players
        for player_id in data.get("playerIds", []):
            player = Player.query.get(player_id)
            if player:
                party.players.append(player)
        db.session.commit()
        return jsonify({
            "id": party.id,
            "name": party.name,
            "players": [
                {"id": player.id, "name": player.name} for player in party.players
            ]
        })

    if request.method == "DELETE":
        db.session.delete(party)
        db.session.commit()
        return jsonify({"message": "Party deleted"})
