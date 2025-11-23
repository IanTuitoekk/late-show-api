import sys
import os

# Add server directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from app import app
from config import db
from models import Episode, Guest, Appearance

@pytest.fixture
def client():
    """Create test client with in-memory database"""
    # Override config before creating tables
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    with app.app_context():
        # Drop all existing tables and create fresh ones
        db.drop_all()
        db.create_all()
        
        # Yield the test client
        with app.test_client() as test_client:
            yield test_client
        
        # Cleanup
        db.session.remove()
        db.drop_all()

@pytest.fixture
def sample_data(client):
    """Add sample data to database"""
    with app.app_context():
        # Create episodes
        e1 = Episode(date="1/11/99", number=1)
        e2 = Episode(date="1/12/99", number=2)
        
        # Create guests
        g1 = Guest(name="Michael J. Fox", occupation="Actor")
        g2 = Guest(name="Sandra Bullock", occupation="Actor")
        
        db.session.add_all([e1, e2, g1, g2])
        db.session.commit()
        
        # Create appearances
        a1 = Appearance(rating=5, episode_id=e1.id, guest_id=g1.id)
        a2 = Appearance(rating=4, episode_id=e1.id, guest_id=g2.id)
        
        db.session.add_all([a1, a2])
        db.session.commit()