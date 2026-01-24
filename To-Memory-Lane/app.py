from flask import Flask, render_template
from flask_login import LoginManager
from config import Config
from models import db, User
from auth import auth_bp
from memories import memories_bp
import os

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(memories_bp, url_prefix='/api')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    os.makedirs('instance', exist_ok=True)
    with app.app_context():
        db.create_all()
    app.run(debug=True)