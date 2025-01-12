from flask import Flask
from flask_cors import CORS
from models import db
from routes.player_routes import player_bp
from routes.party_routes import party_bp
from routes.monster_routes import monster_bp
app = Flask(__name__)
CORS(app)

# Configure the SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dnd_manager.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Register blueprints
app.register_blueprint(player_bp)
app.register_blueprint(party_bp)
app.register_blueprint(monster_bp)


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)


# # Player model
# class Player(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     level = db.Column(db.Integer, nullable=False)
#     ac = db.Column(db.Integer, nullable=False)
#     initiative_modifier = db.Column(db.Integer, nullable=False)

# # Party model
# class Party(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     players = db.relationship('Player', secondary='party_player', backref='parties', lazy='joined')

# # Association table for many-to-many relationship
# party_player = db.Table('party_player',
#     db.Column('party_id', db.Integer, db.ForeignKey('party.id'), primary_key=True),
#     db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True)
# )

# # Monster model
# class Monster(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     size = db.Column(db.String(50))
#     type = db.Column(db.String(50))
#     alignment = db.Column(db.String(50))
#     hp = db.Column(db.Integer)
#     ac = db.Column(db.Integer)
#     speed = db.Column(db.String(100))
#     str = db.Column(db.Integer)
#     dex = db.Column(db.Integer)
#     con = db.Column(db.Integer)
#     int = db.Column(db.Integer)
#     wis = db.Column(db.Integer)
#     cha = db.Column(db.Integer)
#     languages = db.Column(db.String(200))
#     damage_vulnerabilities = db.Column(db.String(200))
#     senses = db.Column(db.String(200))
#     challenge_rating = db.Column(db.Float)
#     actions = db.Column(db.Text)
#     legendary_actions = db.Column(db.Text)
#     traits = db.Column(db.Text)
#     reactions = db.Column(db.Text)

#     def to_dict(self):
#         return {
#             'id': self.id,
#             'name': self.name,
#             'size': self.size,
#             'type': self.type,
#             'alignment': self.alignment,
#             'hp': self.hp,
#             'ac': self.ac,
#             'speed': self.speed,
#             'stats': {
#                 'str': self.str,
#                 'dex': self.dex,
#                 'con': self.con,
#                 'int': self.int,
#                 'wis': self.wis,
#                 'cha': self.cha
#             },
#             'languages': self.languages,
#             'damageVulnerabilities': self.damage_vulnerabilities,
#             'senses': self.senses,
#             'challengeRating': self.challenge_rating,
#             'actions': self.actions,
#             'legendaryActions': self.legendary_actions,
#             'traits': self.traits,
#             'reactions': self.reactions
#         }

# # Create the database and tables
# with app.app_context():
#     db.create_all()

# # Player endpoints
# @app.route("/api/players", methods=["GET", "POST"])
# def manage_players():
#     if request.method == "POST":
#         data = request.json
#         new_player = Player(
#             name=data["name"],
#             level=data["level"],
#             ac=data["ac"],
#             initiative_modifier=data["initiativeModifier"]
#         )
#         db.session.add(new_player)
#         db.session.commit()
#         return jsonify({
#             "id": new_player.id,
#             "name": new_player.name,
#             "level": new_player.level,
#             "ac": new_player.ac,
#             "initiativeModifier": new_player.initiative_modifier
#         }), 201

#     players = Player.query.all()
#     return jsonify([
#         {
#             "id": player.id,
#             "name": player.name,
#             "level": player.level,
#             "ac": player.ac,
#             "initiativeModifier": player.initiative_modifier
#         } for player in players
#     ])

# @app.route("/api/players/<int:player_id>", methods=["PUT", "DELETE"])
# def modify_player(player_id):
#     player = Player.query.get(player_id)
#     if not player:
#         return jsonify({"error": "Player not found"}), 404

#     if request.method == "PUT":
#         data = request.json
#         player.name = data.get("name", player.name)
#         player.level = data.get("level", player.level)
#         player.ac = data.get("ac", player.ac)
#         player.initiative_modifier = data.get("initiativeModifier", player.initiative_modifier)
#         db.session.commit()
#         return jsonify({
#             "id": player.id,
#             "name": player.name,
#             "level": player.level,
#             "ac": player.ac,
#             "initiativeModifier": player.initiative_modifier
#         })

#     if request.method == "DELETE":
#         db.session.delete(player)
#         db.session.commit()
#         return jsonify({"message": "Player deleted"})

# # Party endpoints
# @app.route("/api/parties", methods=["GET", "POST"])
# def manage_parties():
#     if request.method == "POST":
#         data = request.json
#         new_party = Party(name=data["name"])

#         for player_id in data.get("playerIds", []):
#             player = Player.query.get(player_id)
#             if player:
#                 new_party.players.append(player)

#         db.session.add(new_party)
#         db.session.commit()
#         return jsonify({
#             "id": new_party.id,
#             "name": new_party.name,
#             "players": [
#                 {"id": player.id, "name": player.name} for player in new_party.players
#             ]
#         }), 201

#     parties = Party.query.all()
#     return jsonify([
#         {
#             "id": party.id,
#             "name": party.name,
#             "players": [
#                 {"id": player.id, "name": player.name} for player in party.players
#             ]
#         } for party in parties
#     ])

# @app.route("/api/parties/<int:party_id>", methods=["PUT", "DELETE"])
# def modify_party(party_id):
#     party = Party.query.get(party_id)
#     if not party:
#         return jsonify({"error": "Party not found"}), 404

#     if request.method == "PUT":
#         data = request.json
#         party.name = data.get("name", party.name)
#         party.players = []  # Clear current players

#         for player_id in data.get("playerIds", []):
#             player = Player.query.get(player_id)
#             if player:
#                 party.players.append(player)

#         db.session.commit()
#         return jsonify({
#             "id": party.id,
#             "name": party.name,
#             "players": [
#                 {"id": player.id, "name": player.name} for player in party.players
#             ]
#         })

#     if request.method == "DELETE":
#         db.session.delete(party)
#         db.session.commit()
#         return jsonify({"message": "Party deleted"})

# # Monster endpoints
# @app.route('/api/monsters', methods=['GET', 'POST'])
# def manage_monsters():
#     if request.method == 'POST':
#         data = request.json
#         monster = Monster(
#             name=data['name'],
#             size=data['size'],
#             type=data['type'],
#             alignment=data['alignment'],
#             hp=data['hp'],
#             ac=data['ac'],
#             speed=data['speed'],
#             str=data['stats']['str'],
#             dex=data['stats']['dex'],
#             con=data['stats']['con'],
#             int=data['stats']['int'],
#             wis=data['stats']['wis'],
#             cha=data['stats']['cha'],
#             languages=data.get('languages', ''),
#             damage_vulnerabilities=data.get('damageVulnerabilities', ''),
#             senses=data.get('senses', ''),
#             challenge_rating=data.get('challengeRating', 0),
#             actions=data.get('actions', ''),
#             legendary_actions=data.get('legendaryActions', ''),
#             traits=data.get('traits', ''),
#             reactions=data.get('reactions', '')
#         )
#         db.session.add(monster)
#         db.session.commit()
#         return jsonify(monster.to_dict()), 201

#     monsters = Monster.query.all()
#     return jsonify([monster.to_dict() for monster in monsters])

# @app.route('/api/monsters/<int:monster_id>', methods=['PUT', 'DELETE'])
# def modify_monster(monster_id):
#     monster = Monster.query.get(monster_id)
#     if not monster:
#         return jsonify({"error": "Monster not found"}), 404

#     if request.method == 'PUT':
#         data = request.json
#         monster.name = data['name']
#         monster.size = data['size']
#         monster.type = data['type']
#         monster.alignment = data['alignment']
#         monster.hp = data['hp']
#         monster.ac = data['ac']
#         monster.speed = data['speed']
#         monster.str = data['stats']['str']
#         monster.dex = data['stats']['dex']
#         monster.con = data['stats']['con']
#         monster.int = data['stats']['int']
#         monster.wis = data['stats']['wis']
#         monster.cha = data['stats']['cha']
#         monster.languages = data.get('languages', '')
#         monster.damage_vulnerabilities = data.get('damageVulnerabilities', '')
#         monster.senses = data.get('senses', '')
#         monster.challenge_rating = data.get('challengeRating', 0)
#         monster.actions = data.get('actions', '')
#         monster.legendary_actions = data.get('legendaryActions', '')
#         monster.traits = data.get('traits', '')
#         monster.reactions = data.get('reactions', '')

#         db.session.commit()
#         return jsonify(monster.to_dict())

#     if request.method == 'DELETE':
#         db.session.delete(monster)
#         db.session.commit()
#         return jsonify({"message": "Monster deleted"})
