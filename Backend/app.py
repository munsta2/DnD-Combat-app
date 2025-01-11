from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///players.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Player model
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    ac = db.Column(db.Integer, nullable=False)
    initiative_modifier = db.Column(db.Integer, nullable=False)

# Party model
class Party(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    players = db.relationship('Player', secondary='party_player', backref='parties', lazy='joined')

# Association table for many-to-many relationship
party_player = db.Table('party_player',
    db.Column('party_id', db.Integer, db.ForeignKey('party.id'), primary_key=True),
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True)
)

# Create the database and tables
with app.app_context():
    db.create_all()

@app.route("/api/players", methods=["GET", "POST"])
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

@app.route("/api/players/<int:player_id>", methods=["PUT", "DELETE"])
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

@app.route("/api/parties", methods=["GET", "POST"])
def manage_parties():
    if request.method == "POST":
        data = request.json
        new_party = Party(name=data["name"])

        for player_id in data.get("playerIds", []):
            player = Player.query.get(player_id)
            if player:
                new_party.players.append(player)

        db.session.add(new_party)
        db.session.commit()
        return jsonify({
            "id": new_party.id,
            "name": new_party.name,
            "players": [
                {"id": player.id, "name": player.name} for player in new_party.players
            ]
        }), 201

    parties = Party.query.all()
    return jsonify([
        {
            "id": party.id,
            "name": party.name,
            "players": [
                {"id": player.id, "name": player.name} for player in party.players
            ]
        } for party in parties
    ])

@app.route("/api/parties/<int:party_id>", methods=["PUT", "DELETE"])
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

if __name__ == "__main__":
    app.run(debug=True)
