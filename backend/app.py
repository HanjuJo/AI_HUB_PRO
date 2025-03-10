import os
from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_login import LoginManager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, 
            static_folder='static', 
            template_folder='app/templates')

# Configure app
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///ai_hub.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
CORS(app)

# Import models
from app.models.user import User
from app.models.ai_tool import AITool
from app.models.tool_combination import ToolCombination
from app.models.youtube_data import YoutubeData

# Import routes
from app.routes.auth import auth_bp
from app.routes.ai_tools import ai_tools_bp
from app.routes.dashboard import dashboard_bp
from app.routes.youtube import youtube_bp

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(ai_tools_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(youtube_bp)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.template_folder, path)):
        return render_template(path)
    return render_template('index.html')

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
