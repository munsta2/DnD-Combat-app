from flask import Blueprint, jsonify, request

webhook_bp = Blueprint('webhook', __name__)

@app.route('/webhook', methods=['POST'])
def git_update():
    repo = git.Repo('./DnD-Combat-app')
    origin = repo.remotes.origin
    repo.create_head('main',
                     origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
    origin.pull()
    return '', 200