from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

# Initialize the Flask app
app = Flask(_name_)

# Configuration for the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clinic.db'
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this in production
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    availability = db.Column(db.String(100), nullable=False)  # Example format: "Mon-Fri, 9am-5pm"

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    appointment_time = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default="Pending")  # "Pending", "Confirmed", "Cancelled"

# Routes

# Register new user
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(name=data['name'], email=data['email'], phone=data['phone'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully!"}), 201

# Login user
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity={'id': user.id, 'name': user.name})
        return jsonify(access_token=access_token), 200
    return jsonify({"message": "Invalid credentials"}), 401

# Get available doctors
@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    doctors = Doctor.query.all()
    doctor_list = [{"id": doc.id, "name": doc.name, "specialization": doc.specialization, "availability": doc.availability} for doc in doctors]
    return jsonify(doctor_list), 200

# Book an appointment
@app.route('/api/book-appointment', methods=['POST'])
@jwt_required()
def book_appointment():
    data = request.get_json()
    user_id = get_jwt_identity()['id']
    appointment = Appointment(patient_id=user_id, doctor_id=data['doctor_id'], appointment_time=data['appointment_time'])
    db.session.add(appointment)
    db.session.commit()
    return jsonify({"message": "Appointment booked successfully!"}), 201

# Run the app
if _name_ == '_main_':
    db.create_all()  # Creates the database tables if they don't exist
    app.run(debug=True)
