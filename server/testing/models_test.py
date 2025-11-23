import pytest
from app import app
from config import db
from models import Episode, Guest, Appearance

def test_episode_creation(client):
    """Test creating an episode"""
    with app.app_context():
        episode = Episode(date="1/11/99", number=1)
        db.session.add(episode)
        db.session.commit()
        
        assert episode.id is not None
        assert episode.date == "1/11/99"

def test_guest_creation(client):
    """Test creating a guest"""
    with app.app_context():
        guest = Guest(name="Test Guest", occupation="Tester")
        db.session.add(guest)
        db.session.commit()
        
        assert guest.id is not None
        assert guest.name == "Test Guest"

def test_appearance_valid_rating(client, sample_data):
    """Test creating appearance with valid rating"""
    with app.app_context():
        appearance = Appearance(rating=5, episode_id=1, guest_id=1)
        db.session.add(appearance)
        db.session.commit()
        
        assert appearance.rating == 5

def test_appearance_invalid_rating_low(client, sample_data):
    """Test rating validation - too low"""
    with app.app_context():
        with pytest.raises(ValueError):
            appearance = Appearance(rating=0, episode_id=1, guest_id=1)
            db.session.add(appearance)
            db.session.commit()

def test_appearance_invalid_rating_high(client, sample_data):
    """Test rating validation - too high"""
    with app.app_context():
        with pytest.raises(ValueError):
            appearance = Appearance(rating=6, episode_id=1, guest_id=1)
            db.session.add(appearance)
            db.session.commit()

def test_episode_has_appearances(client, sample_data):
    """Test episode has appearances relationship"""
    with app.app_context():
        episode = Episode.query.first()
        assert len(episode.appearances) > 0
        assert episode.appearances[0].guest is not None

def test_cascade_delete_episode(client, sample_data):
    """Test deleting episode deletes appearances"""
    with app.app_context():
        episode = Episode.query.first()
        appearance_count = len(episode.appearances)
        assert appearance_count > 0
        
        db.session.delete(episode)
        db.session.commit()
        
        assert Appearance.query.count() < appearance_count