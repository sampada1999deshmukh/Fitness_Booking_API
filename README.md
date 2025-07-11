### Fitness_Booking_API ###

A Flask REST API for managing fitness class bookings. It supports viewing upcoming classes, booking classes, checking bookings by email, and sending email confirmations.

## Project Setup

#1. Clone the repository
git clone https://github.com/sampada1999deshmukh/Fitness_Booking_API.git
cd Booking_API

#2. Create virtual environment and install dependencies
python -m venv benv
benv\Scripts\activate
pip install -r requirements.txt

#3. Add a .env file in the root folder with the following:
SMTP_EMAIL=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

#4. Seed sample fitness class data
run seed.py (run single file with run button simply)

#5. Run the app
python run.py

#6. API Endpoints

--GET--	
Retrieve all upcoming fitness classes
/check/classes	

--POST--
a fitness class
/check/book	Book 

payload
{"class_id": 1,
  "client_name": "John Doe",
  "client_email": "john@example.com"}

--GET--
Get all bookings by a client's email
/check/bookings/<email> or john@example.com

#7. Run Tests
pytest app/tests/

