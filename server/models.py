from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from config import db


class Episode(db.Model, SerializerMixin):
    __tablename__ = 'episodes'
    
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    number = db.Column(db.Integer)
    
    # Relationships
    appearances = db.relationship('Appearance', back_populates='episode', cascade='all, delete-orphan')
    guests = db.relationship('Guest', secondary='appearances', back_populates='episodes', viewonly=True)
    
    # Serialization rules to prevent infinite recursion
    serialize_rules = ('-appearances.episode', '-guests.episodes')
    
    def __repr__(self):
        return f'<Episode {self.number}: {self.date}>'


class Guest(db.Model, SerializerMixin):
    __tablename__ = 'guests'
    
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    occupation = db.Column(db.String)
    
    # Relationships
    appearances = db.relationship('Appearance', back_populates='guest', cascade='all, delete-orphan')
    episodes = db.relationship('Episode', secondary='appearances', back_populates='guests', viewonly=True)
    
    # Serialization rules to prevent infinite recursion
    serialize_rules = ('-appearances.guest', '-episodes.guests')
    
    def __repr__(self):
        return f'<Guest {self.name}: {self.occupation}>'


class Appearance(db.Model, SerializerMixin):
    __tablename__ = 'appearances'
    
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    
    # Foreign Keys
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'))
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'))
    
    # Relationships
    episode = db.relationship('Episode', back_populates='appearances')
    guest = db.relationship('Guest', back_populates='appearances')
    
    # Serialization rules to prevent infinite recursion
    serialize_rules = ('-episode.appearances', '-guest.appearances')
    
    # Validation: Rating must be between 1 and 5 (inclusive)
    @validates('rating')
    def validate_rating(self, key, rating):
        if rating is None or not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        return rating
    
    def __repr__(self):
        return f'<Appearance {self.id}: Episode {self.episode_id}, Guest {self.guest_id}, Rating {self.rating}>'