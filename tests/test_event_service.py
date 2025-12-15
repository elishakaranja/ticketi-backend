from datetime import datetime, timedelta
from server.services.event_service import create_event
from server.models import User, Event, Ticket

def test_create_event(app, db):
    """Test creating a new event."""
    with app.app_context():
        # 1. Create a test user
        user = User(username='testuser', email='test@test.com', password='password')
        db.session.add(user)
        db.session.commit()

        # 2. Prepare test data
        event_data = {
            'name': 'Test Event',
            'location': 'Test Location',
            'description': 'Test Description',
            'date': (datetime.utcnow() + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'),
            'price': 10.0,
            'capacity': 100
        }

        # 3. Call the create_event service function
        new_event, error = create_event(event_data, user.id)

        # 4. Assert that the event was created correctly
        assert error is None
        assert new_event is not None
        assert new_event.name == 'Test Event'
        assert new_event.organizer.username == 'testuser'

        # 5. Assert that the tickets were created correctly
        assert Ticket.query.count() == 100
