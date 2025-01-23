from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

# Player model
class Player(db.Model):
    __tablename__ = 'player'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    ac = db.Column(db.Integer, nullable=False)
    initiative_modifier = db.Column(db.Integer, nullable=False)
    player_encounters = db.relationship('EncounterPlayer', back_populates='player')
   

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



class EncounterMonster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    encounter_id = db.Column(db.Integer, db.ForeignKey('encounter.id'))
    monster_id = db.Column(db.Integer, db.ForeignKey('monster.id'))
    alias = db.Column(db.String(100))  # Alias for the monster
    count = db.Column(db.Integer, default=1)  # Number of this monster
    # Relationships
    encounter = db.relationship('Encounter', back_populates='encounter_monsters')
    monster = db.relationship('Monster', back_populates='monster_encounters')

class Encounter(db.Model):
    __tablename__ = 'encounter'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    encounter_monsters = db.relationship('EncounterMonster', back_populates='encounter', cascade='all, delete-orphan')
    encounter_players = db.relationship('EncounterPlayer', back_populates='encounter', cascade="all, delete-orphan")

class EncounterPlayer(db.Model):
    __tablename__ = 'encounter_player'

    id = db.Column(db.Integer, primary_key=True)
    encounter_id = db.Column(db.Integer, db.ForeignKey('encounter.id'))
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    alias = db.Column(db.String(100))
    count = db.Column(db.Integer, default=1)

    # Relationships
    encounter = db.relationship('Encounter', back_populates='encounter_players')
    player = db.relationship('Player', back_populates='player_encounters')



class Monster(db.Model):
    __tablename__ = 'monster'
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
    cr = db.Column(db.String(10), nullable=True)  # Challenge Rating (e.g., "1/4")
    exp = db.Column(db.Integer, nullable=True)  # Experience Points (e.g., 50)
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
            'stats': {
                'str': self.str,
                'dex': self.dex,
                'con': self.con,
                'int': self.int,
                'wis': self.wis,
                'cha': self.cha,
            },
            'languages': self.languages,
            'damageVulnerabilities': self.damage_vulnerabilities,
            'senses': self.senses,
            'cr': self.cr,
            'exp': self.exp,
            'actions': self.actions,
            'legendaryActions': self.legendary_actions,
            'traits': self.traits,
            'reactions': self.reactions,
        }
    monster_encounters = db.relationship('EncounterMonster', back_populates='monster')


class ActiveCombat(db.Model):
    __tablename__ = 'active_combat'
    id = db.Column(db.Integer, primary_key=True)
    encounter_id = db.Column(db.Integer, db.ForeignKey('encounter.id'), nullable=False)
    turn_order = db.Column(db.JSON, nullable=False)  # Stores combatants' order
    active_turn_index = db.Column(db.Integer, default=0)