from flask import Blueprint, jsonify, request
from git import Repo
webhook_bp = Blueprint('webhook', __name__)

@webhook_bp.route('/webhook', methods=['POST'])
def git_update():
    repo = git.Repo('./DnD-Combat-app')
    origin = repo.remotes.origin
    repo.create_head('main',
                     origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
    origin.pull()
    return '', 200
    # payload = request.get_json()
    # # Process the payload
    # return jsonify({"status": "success"}), 200