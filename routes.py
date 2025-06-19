from datetime import datetime, time
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify
from flask_login import login_required, LoginManager, current_user, login_user
from app import app
from datetime import datetime
from extensions import db
from werkzeug.security import check_password_hash
from models import CityInfo, PlacesInfo, User, Post, Place, LikedPlace, Rating, Feedback, Trip, TripParticipant,Message
from werkzeug.utils import secure_filename
from models import db, ChatMessage, User
import uuid
import bcrypt
import os

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Redirect to login page if not logged in

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index():
    return render_template("index.html", page="register")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        # Check if the email is already registered
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("User already exists with this email!", "error")
            return render_template("index.html", page="register")

        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        # Create a new user with the name, email, and hashed password
        new_user = User(name=name, email=email, password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            flash("An error occurred while saving the user.", "error")
            return render_template("index.html", page="register")

        return redirect(url_for("login"))

    return render_template("index.html", page="register")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Fetch the user from the database using email
        user = User.query.filter_by(email=email).first()

        # Validate the user's password
        if user and bcrypt.checkpw(password.encode("utf-8"), user.password):
            login_user(user)  # Login the user
            return redirect(url_for("home"))
        else:
            flash("Invalid email or password. Please try again.", "error")
            return redirect(url_for("login"))

    return render_template("index.html", page="login")

@app.route("/home")
def home():
    return render_template("home.html", page="home")

@app.route("/logout")
def logout():
    return redirect(url_for("login"))

@app.route("/india", endpoint="india")
def file1():
    return render_template("india.html")

@app.route("/gallery", endpoint="gallery")
def file2():
    return render_template("gallery.html")

@app.route('/hiddengems')
def hiddengems():
    posts = Post.query.all()
    return render_template('hiddengems.html', posts=posts, current_email=current_user.email)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        place_name = request.form.get('name')
        description = request.form.get('description')
        files = request.files.getlist('images')

        if not place_name or not description:
            flash("Please provide a name and description.", "error")
            return redirect(url_for('upload'))
            file.save(os.path.join('static/images', filename))

        image_paths = []
        for file in files:
            if file:
                unique_filename = f"{uuid.uuid4()}_{file.filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(filepath)
                image_paths.append(unique_filename)

        # Save post to database
        new_post = Post(
            name=place_name,
            description=description,
            image_paths=",".join(image_paths),
            uploader_email=current_user.email
        )
        try:
            db.session.add(new_post)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while saving the post.", "error")
            return redirect(url_for('upload'))

        return redirect(url_for('hiddengems'))

    return render_template('upload.html')

@app.route("/uploads/<filename>")
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/delete/<int:post_id>", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.uploader_email != current_user.email:
        flash("You do not have permission to delete this post.", "error")
        return redirect(url_for("hiddengems"))

    if post.image_paths:
        image_paths = post.image_paths.split(",")
        for path in image_paths:
            try:
                os.remove(os.path.join(app.config["UPLOAD_FOLDER"], path))
            except FileNotFoundError:
                pass

    try:
        db.session.delete(post)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while deleting the post.", "error")

    return redirect(url_for("hiddengems"))


@app.route('/state/<state_name>')
@login_required
def state(state_name):
    # Fetch places for the given state
    places = Place.query.filter_by(state=state_name).all()

    # Prepare data for rendering
    places_data = []
    for place in places:
        # Fetch associated images
        images = [img.url for img in place.images]

        # Calculate average rating (with safe handling for division)
        ratings = Rating.query.filter_by(place_id=place.id).all()
        avg_rating = round(sum(r.stars for r in ratings) / len(ratings), 1) if ratings else 0.0

        # Fetch feedback for the place
        feedbacks = Feedback.query.filter_by(place_id=place.id).all()

        # Add place data to the list
        places_data.append({
            'place': place,
            'images': images,
            'avg_rating': avg_rating,
            'feedbacks': feedbacks
        })

    # Render the state page with the gathered data
    return render_template(
        'state.html',
        state_name=state_name,
        places_data=places_data,
        current_email=current_user.email
    )



@app.route('/liked', methods=['GET', 'POST'])
@login_required
def liked():
    if request.method == 'POST':
        place_id = request.json.get('place_id')
        if not place_id:
            return jsonify({'success': False, 'error': 'No place ID provided'}), 400

        liked_place = LikedPlace.query.filter_by(user_email=current_user.email, place_id=place_id).first()
        if liked_place:
            db.session.delete(liked_place)
            db.session.commit()
            return jsonify({'success': True, 'liked': False})
        else:
            new_like = LikedPlace(user_email=current_user.email, place_id=place_id)
            db.session.add(new_like)
            db.session.commit()
            return jsonify({'success': True, 'liked': True})

    liked_places = LikedPlace.query.filter_by(user_email=current_user.email).all()
    places_data = []

    for liked_place in liked_places:
        place = liked_place.place
        ratings = Rating.query.filter_by(place_id=place.id).all()
        avg_rating = round(sum(r.stars for r in ratings) / len(ratings), 1) if ratings else 0.0
        feedbacks = Feedback.query.filter_by(place_id=place.id).all()

        places_data.append({
            'id': place.id,
            'name': place.name,
            'description': place.description,
            'images': [img.url for img in place.images],
            'rating': avg_rating,
            'feedbacks': feedbacks
        })

    return render_template('liked.html', places_data=places_data, current_email=current_user.email)

@app.route('/toggle_like/<int:place_id>', methods=['POST'])
@login_required
def toggle_like(place_id):
    existing = LikedPlace.query.filter_by(user_email=current_user.email, place_id=place_id).first()

    if existing:
        db.session.delete(existing)
        db.session.commit()
    else:
        new_like = LikedPlace(user_email=current_user.email, place_id=place_id)
        db.session.add(new_like)
        db.session.commit()

    return redirect(url_for('liked_places'))

@app.route('/submit_rating_feedback/<int:place_id>', methods=['POST'])
@login_required
def submit_rating_feedback(place_id):
    rating_value = request.form.get('rating')
    feedback_comment = request.form.get('feedback')

    if rating_value:
        existing_rating = Rating.query.filter_by(user_email=current_user.email, place_id=place_id).first()
        if existing_rating:
            existing_rating.stars = int(rating_value)
        else:
            new_rating = Rating(user_email=current_user.email, place_id=place_id, stars=int(rating_value))
            db.session.add(new_rating)

    if feedback_comment and feedback_comment.strip():
        new_feedback = Feedback(user_email=current_user.email, place_id=place_id, comment=feedback_comment.strip())
        db.session.add(new_feedback)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while submitting your rating/feedback.", "error")

    return redirect(request.referrer)

@app.route('/delete_feedback_and_rating/<int:place_id>', methods=['POST'])
@login_required
def delete_feedback_and_rating(place_id):
    feedback_id = request.form.get('feedback_id')
    feedback = Feedback.query.get(feedback_id)

    if not feedback:
        flash("Feedback not found.", "error")
        return redirect(request.referrer)

    if feedback.user_email != current_user.email:
        flash("You do not have permission to delete this feedback.", "error")
        return redirect(request.referrer)

    try:
        db.session.delete(feedback)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while deleting feedback.", "error")

    return redirect(request.referrer)

# Route to display chat list and messages with a specific user@app.route('/chat', methods=['GET'])
@app.route('/chat', methods=['GET'])
@login_required
def chat():
    # Get the list of users this logged-in user has had a conversation with
    previous_chats = db.session.query(ChatMessage.receiver_email).filter_by(sender_email=current_user.email).union(
        db.session.query(ChatMessage.sender_email).filter_by(receiver_email=current_user.email)).distinct().all()

    chat_users = []
    for chat in previous_chats:
        email = chat[0]
        user = User.query.filter_by(email=email).first()
        if user and user.email != current_user.email:
            chat_users.append(user)

    return render_template('chat.html', chat_users=chat_users)


@app.route('/chat/<receiver_email>', methods=['GET'])
@login_required
def chat_with_user(receiver_email):
    receiver = User.query.filter_by(email=receiver_email).first()
    if not receiver:
        return render_template('error.html', message="User not found")

    # Get all messages between logged-in user and the selected user
    messages = ChatMessage.query.filter(
        ((ChatMessage.sender_email == current_user.email) & (ChatMessage.receiver_email == receiver_email)) |
        ((ChatMessage.sender_email == receiver_email) & (ChatMessage.receiver_email == current_user.email))
    ).order_by(ChatMessage.timestamp.asc()).all()

    return render_template('chat_with_user.html', receiver=receiver, messages=messages)

@app.route('/start_new_chat', methods=['GET', 'POST'])
@login_required
def start_new_chat():
    if request.method == 'POST':
        receiver_email = request.form.get('receiver_email')

        # Ensure the receiver exists
        receiver = User.query.filter_by(email=receiver_email).first()
        if receiver and receiver.email != current_user.email:
            return redirect(url_for('chat_with_user', receiver_email=receiver.email))
        else:
            return render_template('chat.html', error="User not found or you cannot chat with yourself.")
    
    return render_template('chat.html')



@app.route('/send_message', methods=['POST'])
@login_required
def send_message():
    receiver_email = request.form.get('receiver_email')
    message = request.form.get('message')
    file = request.files.get('file')

    receiver = User.query.filter_by(email=receiver_email).first()
    if not receiver:
        return jsonify({"error": "User not found"}), 404

    # Create a new message
    new_message = ChatMessage(
        sender_email=current_user.email,
        receiver_email=receiver_email,
        message=message,
        timestamp=datetime.utcnow()
    )

    # If a file is uploaded, save it
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join('uploads', filename))
        new_message.file = filename

    # Save the message to the database
    db.session.add(new_message)
    db.session.commit()

    return redirect(url_for('chat_with_user', receiver_email=receiver_email))


@app.route('/delete_message/<int:message_id>', methods=['POST'])
@login_required
def delete_message(message_id):
    message = ChatMessage.query.get(message_id)

    if not message:
        return jsonify({"error": "Message not found"}), 404

    if message.sender_email != current_user.email:
        return jsonify({"error": "You do not have permission to delete this message"}), 403

    # Delete the message
    db.session.delete(message)
    db.session.commit()

    return redirect(url_for('chat_with_user', receiver_email=message.receiver_email))

@app.route('/chatbox', methods=['POST'])
def chatbox():
    # Check if the request contains JSON data
    if request.is_json:
        data = request.get_json()
        user_query = data.get('query', '').lower()

        if 'place' in user_query:
            places = PlacesInfo.query.all()
            results = [{"place": p.place, "desc": p.place_desc, "rating": p.ratings} for p in places]
            return jsonify({"response": results})

        if 'city' in user_query:
            cities = CityInfo.query.all()
            results = [{"city": c.city, "desc": c.city_desc, "rating": c.ratings} for c in cities]
            return jsonify({"response": results})

        return jsonify({"response": "I'm sorry, I don't understand your question."})
    
    # If Content-Type is not JSON, return an error
    return jsonify({"error": "Unsupported Media Type. Expected application/json."}), 415


@app.route('/plan_trip', methods=['GET', 'POST'])
@login_required
def plan_trip():
    if request.method == 'POST':
        # Fetch form data
        destination = request.form['destination']
        details = request.form['details']
        date_str = request.form['date']
        
        try:
            max_participants = int(request.form['max_participants'])
            if max_participants <= 0:
                raise ValueError("Max participants must be greater than zero.")
        except ValueError:
            flash("Invalid value for max participants. Please enter a positive number.", "error")
            return redirect(url_for('plan_trip'))

        try:
            # Convert the date string to a date object
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            flash("Invalid date format. Please use YYYY-MM-DD.", "error")
            return redirect(url_for('plan_trip'))

        # Create a new trip
        new_trip = Trip(
            planner_id=current_user.id,
            destination=destination,
            details=details,
            date=date,
            max_participants=max_participants
        )

        db.session.add(new_trip)
        db.session.flush()  # Ensures `new_trip.id` is generated before committing

        # Add the planner as a participant in the trip
        new_participant = TripParticipant(
            trip_id=new_trip.id,
            user_id=current_user.id,
            name="Anonymous",  # Optional: Provide default values for required fields
            phone_number="N/A"
        )
        db.session.add(new_participant)

        # Commit the transaction
        db.session.commit()
        flash("Trip planned successfully! You are automatically added as a participant.", "success")
        return redirect(url_for('trips', trip_id=new_trip.id))

    # Handle GET requests (render the plan trip form)
    return render_template('plan_trip.html')


# Trips Route: View planned and available trips
@app.route('/trips', methods=['GET'])
@login_required
def trips():
    # Fetch trips planned by the current user (My Trips)
    my_trips = Trip.query.filter_by(planner_id=current_user.id).all()

    # Fetch available trips planned by others with participant count and participation status
    other_trips_query = (
        db.session.query(
            Trip, 
            db.func.count(TripParticipant.user_id).label('participants_count')
        )
        .outerjoin(TripParticipant, Trip.id == TripParticipant.trip_id)
        .filter(Trip.planner_id != current_user.id)
        .group_by(Trip.id)
        .all()
    )

    # Process the other trips and check if the current user is already participating
    other_trips = []
    for trip, participants_count in other_trips_query:
        trip.is_user_participating = any(
            participant.user_id == current_user.id for participant in trip.participants
        ) 
        other_trips.append(trip)

    return render_template('trips.html', my_trips=my_trips, other_trips=other_trips)


# Join Trip Route: Join a specific trip
@app.route('/join_trip/<int:trip_id>', methods=['POST'])
@login_required
def join_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)

    # Ensure the trip has not reached the max participants
    if len(trip.participants) >= trip.max_participants:
        flash("Sorry, this trip has reached the maximum number of participants.", "error")
        return redirect(url_for('trips'))

    # Ensure the user isn't already participating in the trip
    if any(participant.user_id == current_user.id for participant in trip.participants):
        flash("You are already a participant of this trip.", "info")
        return redirect(url_for('trips'))

    # Create a new participant entry
    participant = TripParticipant(
    trip_id=trip.id,
    user_id=current_user.id,
    name=request.form.get('name', ''),
    phone_number=request.form.get('phone_number', ''),
    about_me=request.form.get('about_me', ''),
    language=request.form.get('language', ''),
    age=request.form.get('age', '')
)


    # Add the participant and commit to the database
    db.session.add(participant)
    db.session.commit()

    flash("You have successfully joined the trip!", "success")
    return redirect(url_for('trips'))  
# Leave trip route

@app.route('/leave_trip/<int:trip_id>', methods=['POST'])
@login_required
def leave_trip(trip_id):
    participant = TripParticipant.query.filter_by(trip_id=trip_id, user_id=current_user.id).first()
    if not participant:
        flash("You are not part of this trip.", "danger")
        return redirect(url_for('trips', trip_id=trip_id))

    db.session.delete(participant)
    db.session.commit()

    flash("You have left the trip.", "success")
    return redirect(url_for('trips', trip_id=trip_id))

@app.route("/delete_trip/<int:trip_id>", methods=["POST"])
def delete_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)

    # Option 1: Delete the participants first
    for participant in trip.participants:
        db.session.delete(participant)

    # Option 2: Set trip_id to NULL in the participants table (if you don't want to delete them)
    # db.session.execute('UPDATE trip_participant SET trip_id = NULL WHERE trip_id = :trip_id', {'trip_id': trip.id})

    db.session.delete(trip)
    db.session.commit()

    return redirect(url_for('trips'))


