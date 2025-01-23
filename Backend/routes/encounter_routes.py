from flask import Blueprint, request, jsonify
from models import db, Encounter, EncounterPlayer, EncounterMonster

encounter_bp = Blueprint("encounters", __name__)

@encounter_bp.route("/api/encounters", methods=["POST"])
def create_encounter():
    data = request.json
    print("Received encounter data:", data)
    # Create the encounter
    new_encounter = Encounter(name=data['name'])
    db.session.add(new_encounter)
    db.session.flush()   

    ## Add players to the encounter
    for player_id in data.get('player_ids', []):
        encounter_player = EncounterPlayer(
            encounter_id=new_encounter.id,
            player_id=player_id
        )
        db.session.add(encounter_player)

    for monster_data in data.get('monsters', []):
        encounter_monster = EncounterMonster(
            encounter_id=new_encounter.id,
            monster_id=monster_data['id'],
            alias=monster_data.get('alias', ''),
            count=1  # You can adjust this if your frontend supports specifying count
        )
        db.session.add(encounter_monster)

    db.session.commit()
    return jsonify({'message': 'Encounter created successfully', 'encounter_id': new_encounter.id}), 201






@encounter_bp.route('/api/encounters', methods=['GET'])
def get_encounters():
    encounters = Encounter.query.all()
    return jsonify([
        {
            'id': encounter.id,
            'name': encounter.name,
            'monsters': [
                {
                    'id': em.monster.id,
                    'name': em.monster.name,
                    'hp': em.monster.hp,
                    'ac': em.monster.ac,
                    'dex': em.monster.dex,
                    'alias': em.alias,
                    'count': em.count
                }
                for em in encounter.encounter_monsters
            ],
            'players': [
                {
                    'id': ep.player.id,
                    'name': ep.player.name,
                    'ac': ep.player.ac,
                    'alias': ep.alias,
                    'count': ep.count
                }
                for ep in encounter.encounter_players
            ]
        }
        for encounter in encounters
    ])
