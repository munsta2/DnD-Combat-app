from flask import Blueprint, jsonify, request
import os
import git

webhook_bp = Blueprint('webhook', __name__)

@webhook_bp.route('/webhook', methods=['POST'])
def git_update():
        # Dynamically resolve the repository path
        REPO_PATH = os.path.join(os.path.dirname(__file__), '../../')
        repo = Repo(REPO_PATH)
        repo.create_head('main(venv)',origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
        # Pull latest changes
        origin = repo.remotes.origin
        origin.pull()

        return 'Pull successful', 200

@webhook_bp.route('/webhook', methods=['GET'])
def get_repo():
    REPO_PATH = os.path.join(os.path.dirname(__file__), '../../')

    try:
        repo = git.Repo(REPO_PATH)  # Replace with your repo path
        current_branch = repo.active_branch.name
        print(f"Current branch: {current_branch}")
        return f"Current branch: {current_branch}", 200  # Return branch name as response with status code 200
    except Exception as e:
        print(f"Error: {e}")
        return f"An error occurred: {e}", 500  # Return error message with status code 500
