from app import db
import os
from .models import User,FitnessClass,Booking
from flask import jsonify
from datetime import datetime
import re
from pytz import timezone, utc
from pytz import timezone
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

def get_all_upcoming_classes():
    try:
        now_utc = datetime.utcnow()
        classes = FitnessClass.query.filter(FitnessClass.date_time > now_utc).all()

        if not classes:
            return jsonify({"msg": "No upcoming classes found", "data": []}), 200

        ist = timezone('Asia/Kolkata')
        class_list = []
        for cls in classes:
            # Step 1: Convert stored UTC to IST
            dt_ist = cls.date_time.astimezone(ist)

            class_list.append({
                "name": cls.name,
                "date": dt_ist.date().isoformat(),
                "time": dt_ist.time().isoformat(timespec='minutes'),
                "instructor": cls.instructor,
                "available_slots": cls.available_slots
            })

        return jsonify({"msg": "Upcoming classes fetched successfully", "data": class_list}), 200

    except Exception as e:
        logger.error(f"Error fetching classes: {str(e)}")
        return jsonify({"msg": f"Error occurred while getting class details: {str(e)}"}), 500

def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    return re.match(pattern, email)

def send_email_notification(to_email, subject, body):
    try:
        smtp_email = os.getenv('SMTP_EMAIL')
        smtp_password = os.getenv('SMTP_PASSWORD')
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', 587))

        if not smtp_email or not smtp_password:
            logger.warning("SMTP credentials not found. Skipping email.")
            return

        msg = MIMEMultipart()
        msg['From'] = smtp_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_email, smtp_password)
        server.sendmail(smtp_email, to_email, msg.as_string())
        server.quit()

        logger.info(f"Email sent successfully to {to_email}")
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")


def make_booking(data):
    try:
        class_id = data.get('class_id')
        client_name = data.get('client_name')
        client_email = data.get('client_email')

        if not all([class_id, client_name, client_email]):
            return jsonify({"msg": "Missing required fields"}), 400

        client_email = client_email.strip().lower()
        client_name = client_name.strip()

        if not is_valid_email(client_email):
            return jsonify({"msg": "Invalid email format"}), 400

        if len(client_name) < 4:
            return jsonify({"msg": "Client name must be at least 4 characters"}), 400

        previous_booking = Booking.query.filter_by(client_email=client_email).first()
        if previous_booking:
            if previous_booking.client_name.strip().lower() != client_name.lower():
                return jsonify({
                    "msg": f"This email is already associated with '{previous_booking.client_name}' "
                           f"Please use the correct name."}), 409

        fitness_class = FitnessClass.query.get(class_id)
        if not fitness_class:
            return jsonify({"msg": "Class not found"}), 404

        already_booked = Booking.query.filter_by(class_id=class_id, client_email=client_email).first()
        if already_booked:
            return jsonify({"msg": "You have already booked this class."}), 409

        overlapping_booking = (
            db.session.query(Booking)
            .join(FitnessClass, FitnessClass.id == Booking.class_id)
            .filter(
                Booking.client_email == client_email,
                FitnessClass.date_time == fitness_class.date_time).first())
        if overlapping_booking:
            return jsonify({
                "msg": f"You already have another class booked at {fitness_class.date_time.strftime('%Y-%m-%d %H:%M')}."
            }), 409

        if fitness_class.available_slots <= 0:
            return jsonify({"msg": "No slots available"}), 400

        fitness_class.available_slots -= 1

        booking = Booking(
            class_id=class_id,
            client_name=client_name,
            client_email=client_email,
            booked_at=datetime.now(utc))

        db.session.add(booking)
        db.session.commit()

        subject = "Fitness Class Booking Confirmation"
        body = f"""
               Hi {client_name},

               Your booking for the class '{fitness_class.name}' on {fitness_class.date_time.strftime('%Y-%m-%d %H:%M')} has been confirmed.

               Thank you!
               """
        send_email_notification("sampada1999deshmukh@gmail.com", subject, body)

        logger.info(f"Class booked successfully: {booking}")

        return jsonify({
            "msg": "Booking successful",
            "booking": booking.to_dict()}), 201

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error while booking class: {str(e)}")
        return jsonify({"msg": f"Error occurred while booking: {str(e)}"}), 500

def get_bookings_by_email(email):
    try:
        bookings = Booking.query.filter_by(client_email=email).all()
        if not bookings:
            return {"msg": "No bookings found for this email."}, 404

        result = []
        ist = timezone('Asia/Kolkata')

        for booking in bookings:
            fitness_class = FitnessClass.query.get(booking.class_id)
            if not fitness_class:
                continue

            utc_dt = fitness_class.date_time.replace(tzinfo=utc)
            ist_dt = utc_dt.astimezone(ist)

            result.append({
                "booking_id": booking.id,
                "class_id": booking.class_id,
                "class_name": fitness_class.name,
                "class_date": ist_dt.strftime('%Y-%m-%d'),
                "class_time": ist_dt.strftime('%H:%M:%S'),
                "client_name": booking.client_name,
                "client_email": booking.client_email})

        return result, 200

    except Exception as e:
        logger.error(f"Error fetching classes Details: {str(e)}")
        return {"msg": f"Error while fetching bookings: {str(e)}"}, 500