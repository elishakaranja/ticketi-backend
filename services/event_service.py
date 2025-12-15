from datetime import datetime
from models import db, Event, Ticket

def create_event(data, user_id):
    """Creates a new event and its associated tickets."""
    try:
        event_date = datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S')
        if event_date <= datetime.utcnow():
            return None, {'error': 'Event date must be in the future'}

        price = float(data['price'])
        capacity = int(data['capacity'])
        if price < 0:
            return None, {'error': 'Price cannot be negative'}
        if capacity <= 0:
            return None, {'error': 'Capacity must be greater than 0'}

        new_event = Event(
            name=data['name'],
            location=data['location'],
            location_lat=data.get('location_lat'),
            location_lng=data.get('location_lng'),
            description=data['description'],
            date=event_date,
            price=price,
            capacity=capacity,
            image=data.get('image'),
            user_id=user_id,
            status='upcoming'
        )
        
        db.session.add(new_event)
        db.session.commit()

        tickets = []
        for _ in range(capacity):
            ticket = Ticket(
                event_id=new_event.id,
                price=price,
                status='available'
            )
            tickets.append(ticket)
        
        db.session.bulk_save_objects(tickets)
        db.session.commit()

        return new_event, None

    except (ValueError, TypeError):
        return None, {'error': 'Invalid price, capacity, or date format'}
    except Exception as e:
        db.session.rollback()
        # In a real app, you'd want to log this error
        return None, {'error': f'Failed to create event: {str(e)}'}

def update_event(event, data):
    """Updates an event."""
    try:
        if 'name' in data:
            event.name = data['name']
        if 'location' in data:
            event.location = data['location']
        if 'location_lat' in data:
            event.location_lat = data['location_lat']
        if 'location_lng' in data:
            event.location_lng = data['location_lng']
        if 'description' in data:
            event.description = data['description']
        if 'date' in data:
            event.date = datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S')
        if 'price' in data:
            event.price = float(data['price'])
        if 'image' in data:
            event.image = data['image']
        if 'status' in data:
            event.status = data['status']

        db.session.commit()
        return event, None

    except (ValueError, TypeError):
        return None, {'error': 'Invalid data format'}
    except Exception as e:
        db.session.rollback()
        # In a real app, you'd want to log this error
        return None, {'error': f'Failed to update event: {str(e)}'}

def delete_event(event):
    """Deletes an event."""
    try:
        db.session.delete(event)
        db.session.commit()
        return True, None
    except Exception as e:
        db.session.rollback()
        # In a real app, you'd want to log this error
        return False, {'error': f'Failed to delete event: {str(e)}'}
