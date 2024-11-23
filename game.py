from flask import Flask
from routes.userroutes import user_bp
from routes.gameroute import game_bp
import secrets
app = Flask(__name__)


app.secret_key = secrets.token_hex(24)
# Register blueprints
app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(game_bp, url_prefix="/game")

if __name__ == "__main__":
    app.run(debug=True)
