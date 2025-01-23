from flask import Blueprint, request, jsonify
from models import db, ActiveCombat, Encounter
from random import randint

combat_bp = Blueprint('combat', __name__)

@combat_bp.route('/api/combat/start', methods=['POST'])
def start_combat():
    data = request.json
    encounter_id = data.get('encounter_id')
    encounter = Encounter.query.get(encounter_id)

    if not encounter:
        return jsonify({'error': 'Encounter not found'}), 404

    # Build initial turn order using EncounterPlayer and EncounterMonster relationships
    combatants = []

    # Add players from EncounterPlayer
    for ep in encounter.encounter_players:
        combatants.append({
            'id': ep.player.id,
            'name': ep.player.name,
            'type': 'player',
            'ac': ep.player.ac,
            'initiative': 0
        })

    # Add monsters from EncounterMonster
    for em in encounter.encounter_monsters:
        combatants.append({
            'id': em.monster.id,
            'name': em.monster.name,
            'type': 'monster',
            'hp': em.monster.hp,
            'dex': em.monster.dex,
            'maxHp': em.monster.hp,
            'ac': em.monster.ac,
            'alias': em.alias,
            'count': em.count,
            'initiative': 0
        })

    # Randomize initiative
    for c in combatants:
        c['initiative'] = randint(1, 20)

    # Sort combatants by initiative in descending order
    combatants.sort(key=lambda x: x['initiative'], reverse=True)

    # Create a new ActiveCombat entry
    active_combat = ActiveCombat(
        encounter_id=encounter.id,
        turn_order=combatants,
        active_turn_index=0
    )
    db.session.add(active_combat)
    db.session.commit()

    return jsonify({
        'combat_id': active_combat.id,
        'turn_order': combatants
    })

@combat_bp.route('/api/combat/<int:combat_id>', methods=['GET'])
def get_combat(combat_id):
    combat = ActiveCombat.query.get(combat_id)
    if not combat:
        return jsonify({'error': 'Combat session not found'}), 404

    return jsonify({
        'combat_id': combat.id,
        'encounter_id': combat.encounter_id,
        'turn_order': combat.turn_order,
        'active_turn_index': combat.active_turn_index
    })
@combat_bp.route('/api/combat/<int:combat_id>/update_hp', methods=['POST'])
def update_hp(combat_id):
    data = request.json
    combat = ActiveCombat.query.get(combat_id)

    if not combat:
        return jsonify({'error': 'Combat session not found'}), 404

    combatant_id = data.get('combatant_id')
    hp_change = data.get('hp_change')

    for combatant in combat.turn_order:
        if combatant['id'] == combatant_id:
            combatant['hp'] = max(0, min(combatant['max_hp'], combatant['hp'] + hp_change))
            break

    db.session.commit()
    return jsonify({'message': 'HP updated successfully'})
