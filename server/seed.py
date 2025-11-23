#!/usr/bin/env python3

from app import app
from models import db, Episode, Guest, Appearance

def seed_data():
    with app.app_context():
        # Clear existing data
        print("Clearing existing data...")
        Appearance.query.delete()
        Episode.query.delete()
        Guest.query.delete()
        
        # Create Episodes
        print("Creating episodes...")
        episode1 = Episode(date="1/11/99", number=1)
        episode2 = Episode(date="1/12/99", number=2)
        episode3 = Episode(date="1/13/99", number=3)
        episode4 = Episode(date="1/14/99", number=4)
        episode5 = Episode(date="1/15/99", number=5)
        
        episodes = [episode1, episode2, episode3, episode4, episode5]
        db.session.add_all(episodes)
        
        # Create Guests
        print("Creating guests...")
        guest1 = Guest(name="Michael J. Fox", occupation="Actor")
        guest2 = Guest(name="Sandra Bullock", occupation="Actor")
        guest3 = Guest(name="Bill Gates", occupation="Entrepreneur")
        guest4 = Guest(name="Maya Angelou", occupation="Poet")
        guest5 = Guest(name="Neil deGrasse Tyson", occupation="Astrophysicist")
        guest6 = Guest(name="Oprah Winfrey", occupation="Media Executive")
        
        guests = [guest1, guest2, guest3, guest4, guest5, guest6]
        db.session.add_all(guests)
        
        # Commit to get IDs
        db.session.commit()
        
        # Create Appearances
        print("Creating appearances...")
        appearance1 = Appearance(rating=5, episode_id=episode1.id, guest_id=guest1.id)
        appearance2 = Appearance(rating=4, episode_id=episode1.id, guest_id=guest2.id)
        appearance3 = Appearance(rating=5, episode_id=episode2.id, guest_id=guest3.id)
        appearance4 = Appearance(rating=3, episode_id=episode2.id, guest_id=guest4.id)
        appearance5 = Appearance(rating=5, episode_id=episode3.id, guest_id=guest5.id)
        appearance6 = Appearance(rating=4, episode_id=episode3.id, guest_id=guest1.id)
        appearance7 = Appearance(rating=5, episode_id=episode4.id, guest_id=guest6.id)
        appearance8 = Appearance(rating=4, episode_id=episode4.id, guest_id=guest2.id)
        appearance9 = Appearance(rating=3, episode_id=episode5.id, guest_id=guest3.id)
        appearance10 = Appearance(rating=5, episode_id=episode5.id, guest_id=guest4.id)
        
        appearances = [
            appearance1, appearance2, appearance3, appearance4, appearance5,
            appearance6, appearance7, appearance8, appearance9, appearance10
        ]
        db.session.add_all(appearances)
        
        # Commit all changes
        db.session.commit()
        
        print("✅ Seeding complete!")
        print(f"   - {len(episodes)} episodes created")
        print(f"   - {len(guests)} guests created")
        print(f"   - {len(appearances)} appearances created")

if __name__ == '__main__':
    seed_data()