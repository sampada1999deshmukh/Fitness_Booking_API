from flask import Blueprint,request,jsonify
from .service import *

bp = Blueprint('check', __name__, url_prefix='/check')


@bp.route('/classes', methods=['GET'])
def get_classes():
    classes = get_all_upcoming_classes()
    return classes

@bp.route('/book', methods=['POST'])
def book_class():
    data = request.get_json()
    if not data:
        return jsonify({"msg": "Missing JSON in request"}), 400
    return make_booking(data)


@bp.route('/bookings/<email>', methods=['GET'])
def bookings_by_email(email):
    if not email:
        return jsonify({"msg": "Email parameter is required"}), 400

    result, status = get_bookings_by_email(email)
    return jsonify(result), status

