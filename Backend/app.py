from flask import Flask
from flask_cors import CORS
from models import db
from flask_migrate import Migrate
from routes.player_routes import player_bp
from routes.party_routes import party_bp
from routes.monster_routes import monster_bp
from routes.encounter_routes import encounter_bp
from routes.combat_routes import combat_bp
import git
app = Flask(__name__)
CORS(app)

# Optional: Limit CORS to your Netlify domain for security
CORS(app, resources={r"/*": {"origins": "https://dnd-combat-management.netlify.app"}})


# Configure the SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dnd_manager.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
migrate = Migrate(app, db)
# Register blueprints
app.register_blueprint(player_bp)
app.register_blueprint(party_bp)
app.register_blueprint(monster_bp)
app.register_blueprint(encounter_bp)
app.register_blueprint(combat_bp)


with app.app_context():
    db.create_all()

@app.route('/git_update', methods=['POST'])
def git_update():
    repo = git.Repo('./DnD-Combat-app')
    origin = repo.remotes.origin
    repo.create_head('main',
                     origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
    origin.pull()
    return '', 200
@app.route('/git_update', methods=['GET'])
def get_repo():
    # REPO_PATH = os.path.join(os.path.dirname(__file__), '../../')

    try:
        repo = git.Repo('./DnD-Combat-app')
        current_branch = repo.active_branch.name
        print(f"Current branch: {current_branch}")
        return f"Current branch: {current_branch}", 200  # Return branch name as response with status code 200
    except Exception as e:
        print(f"Error: {e}")
        return f"An error occurred: {e}", 500  # Return error message with status code 500

@app.route('/')
def index():
    test = "checking webhook"
    return test
if __name__ == "__main__":
    app.run(debug=True)

