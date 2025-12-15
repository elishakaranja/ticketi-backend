from datetime import datetime
from models import db, Event, Ticket, Transaction

def purchase_ticket(event_id, user_id):
    """Purchases a ticket for an event."""
    event = Event.query.get(event_id)
    if not event:
        return None, {'error': 'Event not found'}

    if event.date < datetime.utcnow():
        return None, {'error': 'Event has already taken place'}

    ticket = Ticket.query.filter_by(
        event_id=event_id,
        status='available'
    ).first()

    if not ticket:
        return None, {'error': 'No tickets available'}

    try:
        ticket.status = 'sold'
        ticket.user_id = user_id
        ticket.purchase_date = datetime.utcnow()

        transaction = Transaction(
            ticket_id=ticket.id,
            seller_id=event.user_id,
            buyer_id=user_id,
            price=ticket.price,
            transaction_type='primary',
            status='completed'
        )

        event.tickets_sold += 1

        db.session.add(transaction)
        db.session.commit()

        return ticket, None

    except Exception as e:
        db.session.rollback()
        # In a real app, you'd want to log this error
        return None, {'error': f'Failed to purchase ticket: {str(e)}'}

def resell_ticket(ticket, user_id, price):
    """Puts a ticket up for resale."""
    if ticket.user_id != user_id:
        return None, {'error': 'Unauthorized'}

    if ticket.status != 'sold':
        return None, {'error': 'Ticket cannot be resold'}

    if ticket.event.date < datetime.utcnow():
        return None, {'error': 'Event has already taken place'}

    try:
        ticket.status = 'resale'
        ticket.resale_price = price
        db.session.commit()

        return ticket, None

    except Exception as e:
        db.session.rollback()
        # In a real app, you'd want to log this error
        return None, {'error': f'Failed to list ticket for resale: {str(e)}'}

def purchase_resale_ticket(ticket, user_id):
    """Purchases a resale ticket."""
    if ticket.status != 'resale':
        return None, {'error': 'Ticket is not available for resale'}

    if ticket.user_id == user_id:
        return None, {'error': 'Cannot purchase your own ticket'}

    if ticket.event.date < datetime.utcnow():
        return None, {'error': 'Event has already taken place'}

    try:
        transaction = Transaction(
            ticket_id=ticket.id,
            seller_id=ticket.user_id,
            buyer_id=user_id,
            price=ticket.resale_price,
            transaction_type='resale',
            status='completed'
        )

        ticket.status = 'sold'
        ticket.user_id = user_id
        ticket.purchase_date = datetime.utcnow()
        ticket.resale_price = None

        db.session.add(transaction)
        db.session.commit()

        return ticket, None

    except Exception as e:
        db.session.rollback()
        # In a real app, you'd want to log this error
        return None, {'error': f'Failed to purchase resale ticket: {str(e)}'}

def cancel_resale(ticket, user_id):
    """Cancels a ticket's resale listing."""
    if ticket.user_id != user_id:
        return None, {'error': 'Unauthorized'}

    if ticket.status != 'resale':
        return None, {'error': 'Ticket is not listed for resale'}

    try:
        ticket.status = 'sold'
        ticket.resale_price = None
        db.session.commit()

        return ticket, None

    except Exception as e:
        db.session.rollback()
        # In a real app, you'd want to log this error
        return None, {'error': f'Failed to cancel resale listing: {str(e)}'}
