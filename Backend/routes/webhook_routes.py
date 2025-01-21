from flask import Blueprint, jsonify, request
import os
from git import Repo

webhook_bp = Blueprint('webhook', __name__)

@webhook_bp.route('/webhook', methods=['POST'])
def git_update():
    try:
        # Dynamically resolve the repository path
        REPO_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
        repo = Repo(REPO_PATH)

        # Pull latest changes
        origin = repo.remotes.origin
        origin.pull()

        return 'Pull successful', 200
    except Exception as e:
        return f'Error: {e}', 500
