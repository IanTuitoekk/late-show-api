from flask import Flask, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
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


# GET /episodes
class Episodes(Resource):
    def get(self):
        episodes = Episode.query.all()
        return [{'id': e.id, 'date': e.date, 'number': e.number} for e in episodes], 200


# GET /episodes/<int:id> and DELETE /episodes/<int:id>
class EpisodeByID(Resource):
    def get(self, id):
        episode = Episode.query.get(id)
        if not episode:
            return {'error': 'Episode not found'}, 404
        
        return {
            'id': episode.id,
            'date': episode.date,
            'number': episode.number,
            'appearances': [{
                'id': a.id,
                'rating': a.rating,
                'episode_id': a.episode_id,
                'guest_id': a.guest_id,
                'guest': {
                    'id': a.guest.id,
                    'name': a.guest.name,
                    'occupation': a.guest.occupation
                }
            } for a in episode.appearances]
        }, 200
    
    def delete(self, id):
        episode = Episode.query.get(id)
        if not episode:
            return {'error': 'Episode not found'}, 404
        
        db.session.delete(episode)
        db.session.commit()
        return '', 204


# GET /guests
class Guests(Resource):
    def get(self):
        guests = Guest.query.all()
        return [{'id': g.id, 'name': g.name, 'occupation': g.occupation} for g in guests], 200


# POST /appearances
class Appearances(Resource):
    def post(self):
        data = request.get_json()
        
        rating = data.get('rating')
        episode_id = data.get('episode_id')
        guest_id = data.get('guest_id')
        
        # Validate required fields
        if rating is None or episode_id is None or guest_id is None:
            return {'errors': ['rating, episode_id, and guest_id are required']}, 400
        
        # Check if episode and guest exist
        episode = Episode.query.get(episode_id)
        guest = Guest.query.get(guest_id)
        
        if not episode:
            return {'errors': ['Episode not found']}, 400
        if not guest:
            return {'errors': ['Guest not found']}, 400
        
        try:
            new_appearance = Appearance(
                rating=rating,
                episode_id=episode_id,
                guest_id=guest_id
            )
            
            db.session.add(new_appearance)
            db.session.commit()
            
            return {
                'id': new_appearance.id,
                'rating': new_appearance.rating,
                'episode_id': new_appearance.episode_id,
                'guest_id': new_appearance.guest_id,
                'episode': {
                    'id': episode.id,
                    'date': episode.date,
                    'number': episode.number
                },
                'guest': {
                    'id': guest.id,
                    'name': guest.name,
                    'occupation': guest.occupation
                }
            }, 201
            
        except ValueError as e:
            db.session.rollback()
            return {'errors': [str(e)]}, 400


# Register resources
api.add_resource(Episodes, '/episodes')
api.add_resource(EpisodeByID, '/episodes/<int:id>')
api.add_resource(Guests, '/guests')
api.add_resource(Appearances, '/appearances')


# Run the app on port 5555
if __name__ == '__main__':
    app.run(port=5555, debug=True)