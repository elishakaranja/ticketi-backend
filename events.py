from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from models import db, Event, Ticket, User
from sqlalchemy import or_
from services.event_service import create_event as create_event_service, update_event as update_event_service, delete_event as delete_event_service

events_bp = Blueprint('events', __name__)

def is_valid_date(date_str): #helper function to check if the date is after now
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        return date > datetime.utcnow()
    except ValueError:
        return False

@events_bp.route('/', methods=['GET'])
def get_events():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '')
    status = request.args.get('status', 'upcoming')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    category = request.args.get('category')
    
    query = Event.query
    
    if search:
        query = query.filter(
            or_(
                Event.name.ilike(f'%{search}%'),
                Event.description.ilike(f'%{search}%'),
                Event.location.ilike(f'%{search}%')
            )
        )
    
    if status:
        query = query.filter(Event.status == status)

    if start_date:
        query = query.filter(Event.date >= datetime.strptime(start_date, '%Y-%m-%d'))

    if end_date:
        query = query.filter(Event.date <= datetime.strptime(end_date, '%Y-%m-%d'))

    if category:
        query = query.filter(Event.category == category)
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    events = pagination.items
    
    return jsonify({
        'events': [event.to_dict() for event in events],
        'total_pages': pagination.pages,
        'current_page': pagination.page,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev
    }), 200

@events_bp.route('/<int:event_id>', methods=['GET'])
def get_event(event_id):
    event = Event.query.get_or_404(event_id)
    return jsonify(event.to_dict()), 200


########################################



# Create a New Event
@events_bp.route('/', methods=['POST'])
@jwt_required()
def create_event():
    current_user_id = get_jwt_identity()
    data = request.get_json()

    # Validate required fields
    required_fields = ['name', 'location', 'description', 'date', 'price', 'capacity']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

    event, error = create_event_service(data, current_user_id)

    if error:
        return jsonify(error), 400

    return jsonify(event.to_dict()), 201


# Update event 
@events_bp.route('/<int:event_id>', methods=['PUT'])
@jwt_required()
def update_event(event_id):
    current_user_id = get_jwt_identity()
    event = Event.query.get_or_404(event_id)

    # Check if user owns the event
    if event.user_id != current_user_.id:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()

    updated_event, error = update_event_service(event, data)

    if error:
        return jsonify(error), 400

    return jsonify(updated_event.to_dict()), 200


@events_bp.route('/<int:event_id>', methods=['DELETE'])
@jwt_required()
def delete_event(event_id):
    current_user_id = get_jwt_identity()
    event = Event.query.get_or_404(event_id)

    # Check if user owns the event
    if event.user_id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    success, error = delete_event_service(event)

    if error:
        return jsonify(error), 500

    return jsonify({'message': 'Event deleted successfully'}), 200

@events_bp.route('/my-events', methods=['GET'])
@jwt_required()
def get_my_events():
    current_user_id = get_jwt_identity()
    events = Event.query.filter_by(user_id=current_user_id).all()
    return jsonify([event.to_dict() for event in events]), 200 

