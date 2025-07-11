from app import db, create_app
from app.fitness_booking_api.models import FitnessClass
from datetime import datetime
from pytz import timezone

IST = timezone('Asia/Kolkata')
app = create_app()

seed_classes = [
    FitnessClass(name="Zumba", date_time=IST.localize(datetime(2025, 7, 18, 7, 30)), instructor="Sakshi", total_slots=15, available_slots=12),
    FitnessClass(name="Yoga", date_time=IST.localize(datetime(2025, 7, 19, 9, 0)), instructor="Snehal", total_slots=20, available_slots=20),
    FitnessClass(name="Yoga", date_time=IST.localize(datetime(2025, 7, 20, 7, 0)), instructor="Snehal", total_slots=10, available_slots=7),
    FitnessClass(name="Zumba", date_time=IST.localize(datetime(2025, 7, 12, 8, 0)), instructor="Ram", total_slots=12, available_slots=10),
    FitnessClass(name="HIIT", date_time=IST.localize(datetime(2025, 7, 13, 6, 30)), instructor="Divya", total_slots=20, available_slots=18),
]

if __name__ == "__main__":
    with app.app_context():  #
        db.create_all()
        db.session.bulk_save_objects(seed_classes)
        db.session.commit()
        print("Fitness classes inserted successfully!")
