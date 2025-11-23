from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from config import db

# Configure Flask app
app = Flask(__name__)

# Set database URI to SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with app
db.init_app(app)

# Import models AFTER db.init_app() to avoid circular imports
from models import Episode, Guest, Appearance

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Initialize Flask-RESTful
api = Api(app)

# Basic index route to verify server works
@app.route('/')
def index():
    return '<h1>Flask Server Running!</h1>'



# Run the app on port 5555
if __name__ == '__main__':
    app.run(port=5555, debug=True)