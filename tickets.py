from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from server.models import db, Event, Ticket, Transaction, User
from sqlalchemy import and_
from server.services.ticket_service import purchase_ticket as purchase_ticket_service, resell_ticket as resell_ticket_service, purchase_resale_ticket as purchase_resale_ticket_service, cancel_resale as cancel_resale_service

tickets_bp = Blueprint('tickets', __name__)

@tickets_bp.route('/available/<int:event_id>', methods=['GET'])
def get_available_tickets(event_id):
    """Get available tickets for an event"""
    event = Event.query.get_or_404(event_id)
    available_tickets = Ticket.query.filter_by(
        event_id=event_id,
        status='available'
    ).count()

    return jsonify({
        'event': event.to_dict(),
        'available_tickets': available_tickets
    }), 200



@tickets_bp.route('/purchase/<int:event_id>', methods=['POST'])
@jwt_required()
def purchase_ticket(event_id):
    """Purchase a ticket for an event"""
    current_user_id = get_jwt_identity()

    ticket, error = purchase_ticket_service(event_id, current_user_id)

    if error:
        return jsonify(error), 400

    return jsonify({
        'message': 'Ticket purchased successfully',
        'ticket_id': ticket.id,
        'transaction_id': ticket.transactions[-1].id
    }), 201

@tickets_bp.route('/my-tickets', methods=['GET'])
@jwt_required()
def get_my_tickets():
    """Get all tickets owned by the current user"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    current_user_id = get_jwt_identity()
    
    query = Ticket.query.filter_by(user_id=current_user_id)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    tickets = pagination.items
    
    return jsonify({
        'tickets': [{
            'ticket_id': ticket.id,
            'event': ticket.event.to_dict(),
            'status': ticket.status,
            'purchase_date': ticket.purchase_date.isoformat() if ticket.purchase_date else None,
            'price': ticket.price,
            'resale_price': ticket.resale_price
        } for ticket in tickets],
        'total_pages': pagination.pages,
        'current_page': pagination.page,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev
    }), 200



@tickets_bp.route('/resell/<int:ticket_id>', methods=['POST'])
@jwt_required()
def resell_ticket(ticket_id):
    """Put a ticket up for resale"""
    current_user_id = get_jwt_identity()
    data = request.get_json()

    if 'price' not in data or not isinstance(data['price'], (int, float)) or data['price'] < 0:
        return jsonify({'error': 'Invalid resale price'}), 400

    ticket = Ticket.query.get_or_404(ticket_id)

    resold_ticket, error = resell_ticket_service(ticket, current_user_id, data['price'])

    if error:
        return jsonify(error), 400

    return jsonify({
        'message': 'Ticket listed for resale',
        'ticket_id': resold_ticket.id,
        'resale_price': resold_ticket.resale_price
    }), 200

@tickets_bp.route('/resale/<int:event_id>', methods=['GET'])
def get_resale_tickets(event_id):
    """Get all tickets available for resale for an event"""
    resale_tickets = Ticket.query.filter_by(
        event_id=event_id,
        status='resale'
    ).all()
    
    return jsonify([{
        'ticket_id': ticket.id,
        'original_price': ticket.price,
        'resale_price': ticket.resale_price,
        'seller': ticket.owner.username
    } for ticket in resale_tickets]), 200



@tickets_bp.route('/purchase-resale/<int:ticket_id>', methods=['POST'])
@jwt_required()
def purchase_resale_ticket(ticket_id):
    """Purchase a resale ticket"""
    current_user_id = get_jwt_identity()

    ticket = Ticket.query.get_or_404(ticket_id)

    purchased_ticket, error = purchase_resale_ticket_service(ticket, current_user_id)

    if error:
        return jsonify(error), 400

    return jsonify({
        'message': 'Resale ticket purchased successfully',
        'ticket_id': purchased_ticket.id,
        'transaction_id': purchased_ticket.transactions[-1].id
    }), 201



@tickets_bp.route('/cancel-resale/<int:ticket_id>', methods=['POST'])
@jwt_required()
def cancel_resale(ticket_id):
    """Cancel a ticket's resale listing"""
    current_user_id = get_jwt_identity()

    ticket = Ticket.query.get_or_404(ticket_id)

    cancelled_ticket, error = cancel_resale_service(ticket, current_user_id)

    if error:
        return jsonify(error), 400

    return jsonify({
        'message': 'Resale listing cancelled successfully',
        'ticket_id': cancelled_ticket.id
    }), 200 