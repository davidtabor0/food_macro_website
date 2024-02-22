from flask import Flask
from routes import bp
from api import api
from flask_wtf.csrf import CSRFProtect  # Protect site from cross-site request forgery attacks.
from dotenv import load_dotenv
import os

app = Flask(__name__)
csrf = CSRFProtect(app)

# Load the secret key from .env
load_dotenv()
secret_key = os.getenv('SEC_KEY')
app.config['SECRET_KEY'] = secret_key

# Register the blueprint created in routes.py
app.register_blueprint(bp)
app.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)  # Run in debug mode.
