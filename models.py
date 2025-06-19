
from flask_login import UserMixin, current_user
from extensions import db
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)  # Add name field
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_paths = db.Column(db.Text, nullable=False)  # Comma-separated
    uploader_email = db.Column(db.String(150), nullable=False) 
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
# Initialize database

class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    state = db.Column(db.String(100))
    images = db.relationship('PlaceImage', backref='place', lazy=True)
    rating = db.Column(db.Float, default=0.0)

class PlaceImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'), nullable=False)
    # filename = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String, nullable=False)

class LikedPlace(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(100), db.ForeignKey('user.email'), nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'), nullable=False)

    user = db.relationship('User', backref='liked_places')
    place = db.relationship('Place', backref='liked_by')

# Rating model
class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'), nullable=False)
    user_email = db.Column(db.String(150), nullable=False)
    stars = db.Column(db.Integer, nullable=False)

# Feedback model
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'), nullable=False)
    user_email = db.Column(db.String(150), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_email = db.Column(db.String(120), db.ForeignKey('user.email'), nullable=False)
    receiver_email = db.Column(db.String(120), db.ForeignKey('user.email'), nullable=False)
    message = db.Column(db.Text, nullable=True)
    file_path = db.Column(db.String(255), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Message {self.sender_email} -> {self.receiver_email}>'
    
class PlacesInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    place = db.Column(db.String(100), nullable=False)
    ratings = db.Column(db.Float, default=0.0)
    distance = db.Column(db.Float, default=0.0)
    place_desc = db.Column(db.Text, default="Unknown")

class CityInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    ratings = db.Column(db.Float, default=0.0)
    ideal_duration = db.Column(db.Integer, default=0)
    best_time_to_visit = db.Column(db.String(100), default="Unknown")
    city_desc = db.Column(db.Text, default="Unknown")


class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text, nullable=True)
    date = db.Column(db.Date, nullable=False)
    max_participants = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    planner = db.relationship('User', backref='planned_trips')
    participants = db.relationship('TripParticipant', backref='associated_trip', lazy=True)

    @property
    def participants_count(self):
        return len(self.participants)

    def is_user_participating(self):
        return any(participant.user_id == current_user.id for participant in self.participants)



class TripParticipant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False, default='Anonymous')
    phone_number = db.Column(db.String(15), nullable=False, default='0000000000') 
    about_me = db.Column(db.Text, nullable=True)  # Add about me section
    language = db.Column(db.String(50), nullable=True)  # Add language section
    age = db.Column(db.Integer, nullable=True)  # Add age section

    trip = db.relationship('Trip', back_populates='participants',viewonly=True)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    trip = db.relationship('Trip', backref='messages')
    user = db.relationship('User', backref='sent_messages')