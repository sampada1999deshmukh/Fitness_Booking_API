

from app import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    f_name = db.Column(db.String(50), nullable=False)
    l_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            "user_id" : self.user_id,
            "f_name" : self.f_name,
            "l_name" : self.l_name,
            "email" : self.email,
            "role" : self.role
        }
    def __repr__(self):
        return f"<User {self.user_id} >"


class FitnessClass(db.Model):
    __tablename__ = 'fitness_classes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    date_time = db.Column(db.DateTime)
    instructor = db.Column(db.String(50))
    total_slots = db.Column(db.Integer)
    available_slots = db.Column(db.Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "date_time": self.date_time.isoformat(),
            "instructor": self.instructor,
            "total_slots": self.total_slots,
            "available_slots": self.available_slots
        }

    def __repr__(self):
        return f"<FitnessClass {self.name} by {self.instructor} on {self.date_time}>"

class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('fitness_classes.id'))
    client_name = db.Column(db.String(50))
    client_email = db.Column(db.String(120))
    booked_at = db.Column(db.DateTime, default=datetime.utcnow)



    def to_dict(self):
        return {
            "id": self.id,
            "class_id": self.class_id,
            "client_name": self.client_name,
            "client_email": self.client_email,
            "booked_at": self.booked_at.isoformat()
        }

    def __repr__(self):
        return f"<Booking {self.client_name} for class_id {self.class_id}>"


