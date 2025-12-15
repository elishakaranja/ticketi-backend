from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    password_hash = db.Column(db.String(200), nullable = False)  # For storing hashed passwords
    profile_picture = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    events = db.relationship('Event', backref='organizer', lazy=True) #lazy=True means the data is loaded only when accessed (good for performance)
    tickets_owned = db.relationship('Ticket', backref='owner', lazy=True, foreign_keys='Ticket.user_id')
    tickets_sold = db.relationship('Transaction', backref='seller', lazy=True, foreign_keys='Transaction.seller_id')
    tickets_bought = db.relationship('Transaction', backref='buyer', lazy=True, foreign_keys='Transaction.buyer_id')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'profile_picture': self.profile_picture,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    location = db.Column(db.String, nullable = False)
    location_lat = db.Column(db.Float)
    location_lng = db.Column(db.Float)
    description = db.Column(db.String, nullable = False)
    date = db.Column(db.DateTime, nullable = False)  # Changed to DateTime
    price = db.Column(db.Float, nullable = False)
    image = db.Column(db.String)
    capacity = db.Column(db.Integer, nullable = False)  # Total available tickets
    tickets_sold = db.Column(db.Integer, default=0)  # Counter for sold tickets
    status = db.Column(db.String, default='upcoming')  # 'upcoming', 'ongoing', 'completed'
    category = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Relationships
    tickets = db.relationship('Ticket', backref='event', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'location_lat': self.location_lat,
            'location_lng': self.location_lng,
            'description': self.description,
            'date': self.date.strftime('%Y-%m-%d %H:%M:%S') if self.date else None,
            'price': self.price,
            'image': self.image,
            'capacity': self.capacity,
            'tickets_sold': self.tickets_sold,
            'status': self.status,
            'category': self.category,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'user_id': self.user_id
        }

class Ticket(db.Model):
    __tablename__ = 'tickets'
       
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    price = db.Column(db.Float)
    status = db.Column(db.String)  # 'available', 'sold', 'resale'
    resale_price = db.Column(db.Float, nullable=True)  # Price when put up for resale
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    purchase_date = db.Column(db.DateTime, nullable=True)  # When the ticket was bought
    #owner attribute 
    #events attribute 


    # Relationships
    transactions = db.relationship('Transaction', backref='ticket', lazy=True)#Links Ticket to all its Transactions (useful for tracking resales)

class Transaction(db.Model):
    __tablename__ = 'transactions'
       
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'))
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    price = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    transaction_type = db.Column(db.String)  # 'primary' for direct event purchase, 'resale' for user-to-user
    status = db.Column(db.String, default='completed')  # 'pending', 'completed', 'cancelled'

    # In Transaction class (virtual columns created by backrefs):
    # seller -> returns the User who sold the ticket
    # buyer -> returns the User who bought the ticket
    # Example: transaction1.seller or transaction1.buyer



