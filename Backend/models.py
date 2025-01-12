from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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

# Monster model
class Monster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    size = db.Column(db.String(50))
    type = db.Column(db.String(50))
    alignment = db.Column(db.String(50))
    hp = db.Column(db.Integer)
    ac = db.Column(db.Integer)
    speed = db.Column(db.String(100))
    str = db.Column(db.Integer)
    dex = db.Column(db.Integer)
    con = db.Column(db.Integer)
    int = db.Column(db.Integer)
    wis = db.Column(db.Integer)
    cha = db.Column(db.Integer)
    languages = db.Column(db.String(200))
    damage_vulnerabilities = db.Column(db.String(200))
    senses = db.Column(db.String(200))
    challenge_rating = db.Column(db.Float)
    actions = db.Column(db.Text)
    legendary_actions = db.Column(db.Text)
    traits = db.Column(db.Text)
    reactions = db.Column(db.Text)

    def to_dict(self):
     return {
        'id': self.id,
        'name': self.name,
        'size': self.size,
        'type': self.type,
        'alignment': self.alignment,
        'hp': self.hp,
        'ac': self.ac,
        'speed': self.speed,
        'stats': {  # Construct the stats dictionary from individual fields
            'str': self.str,
            'dex': self.dex,
            'con': self.con,
            'int': self.int,
            'wis': self.wis,
            'cha': self.cha
        },
        'languages': self.languages,
        'damageVulnerabilities': self.damage_vulnerabilities,
        'senses': self.senses,
        'challengeRating': self.challenge_rating,
        'actions': self.actions,
        'legendaryActions': self.legendary_actions,
        'traits': self.traits,
        'reactions': self.reactions
    }
