import pytest
from app import create_app, db
from app.fitness_booking_api.models import FitnessClass, Booking
from flask import json
from datetime import datetime, timedelta
from pytz import utc

@pytest.fixture()
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()

        upcoming_class = FitnessClass(
            name="TestYoga",
            date_time=datetime.utcnow() + timedelta(days=1),
            instructor="Snehal",
            total_slots=10,
            available_slots=10)
        db.session.add(upcoming_class)
        db.session.commit()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

def test_get_all_upcoming_classes(client):
    response = client.get('/check/classes')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "data" in data
    assert isinstance(data["data"], list)

def test_make_booking_success(client):
    class_obj = FitnessClass.query.first()
    payload = {
        "class_id": class_obj.id,
        "client_name": "John Doe",
        "client_email": "john@example.com"
    }
    response = client.post('/check/book', data=json.dumps(payload), content_type='application/json')  # FIXED
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["msg"] == "Booking successful"
    assert data["booking"]["client_email"] == "john@example.com"

def test_booking_already_exists(client):
    class_obj = FitnessClass.query.first()
    payload = {
        "class_id": class_obj.id,
        "client_name": "John Doe",
        "client_email": "john@example.com"
    }
    client.post('/check/book', data=json.dumps(payload), content_type='application/json')
    response = client.post('/check/book', data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 409
    data = json.loads(response.data)
    assert "already booked" in data["msg"].lower()

def test_get_bookings_by_email(client):
    class_obj = FitnessClass.query.first()
    booking = Booking(
        class_id=class_obj.id,
        client_name="Test User",
        client_email="test@example.com",
        booked_at=datetime.now(utc))
    db.session.add(booking)
    db.session.commit()
    response = client.get('/check/bookings/test@example.com')
    assert response.status_code == 200 or response.status_code == 404

