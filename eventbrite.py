"""
Eventbrite API endpoints blueprint
Provides access to Eventbrite events data
"""

from flask import Blueprint, jsonify, request
from server.services.eventbrite_service import eventbrite_service

eventbrite_bp = Blueprint('eventbrite', __name__)


@eventbrite_bp.route('/events', methods=['GET'])
def get_eventbrite_events():
    """
    Get events from Eventbrite
    Query params:
        - location: Location string (default: Nairobi, Kenya)
        - category: Category filter
        - page: Page number
        - per_page: Results per page
        - start_date: Start date filter (YYYY-MM-DD)
        - end_date: End date filter (YYYY-MM-DD)
    """
    location = request.args.get('location', 'Nairobi, Kenya')
    category = request.args.get('category')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    result = eventbrite_service.search_events(
        location=location,
        category=category,
        page=page,
        per_page=per_page,
        start_date=start_date,
        end_date=end_date
    )
    
    return jsonify({
        'events': result['events'],
        'total_pages': result['pagination'].get('page_count', 1),
        'current_page': page,
        'source': 'eventbrite'
    })


@eventbrite_bp.route('/events/near-me', methods=['GET'])
def get_nearby_events():
    """
    Get events near a specific location
    Query params:
        - lat: Latitude (required)
        - lng: Longitude (required)
        - radius: Search radius in km (default: 25)
        - category: Category filter
        - limit: Max results (default: 20)
    """
    try:
        lat = float(request.args.get('lat'))
        lng = float(request.args.get('lng'))
    except (TypeError, ValueError):
        return jsonify({'error': 'Valid lat and lng parameters required'}), 400
    
    radius = int(request.args.get('radius', 25))
    category = request.args.get('category')
    limit = int(request.args.get('limit', 20))
    
    events = eventbrite_service.get_events_near_location(
        latitude=lat,
        longitude=lng,
        radius_km=radius,
        category=category,
        limit=limit
    )
    
    return jsonify({
        'events': events,
        'location': {'lat': lat, 'lng': lng},
        'radius_km': radius,
        'source': 'eventbrite'
    })


@eventbrite_bp.route('/events/mixed', methods=['GET'])
def get_mixed_events():
    """
    Get mixed events from both local database and Eventbrite
    Prioritizes Kenya/Nairobi events
    Query params: same as /events endpoint
    """
    from server.models import Event as LocalEvent
    
    # Get query params
    location = request.args.get('location', 'Nairobi, Kenya')
    category = request.args.get('category')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 12))
    search = request.args.get('search', '')
    
    # Fetch local events
    local_query = LocalEvent.query
    
    if search:
        local_query = local_query.filter(
            LocalEvent.name.ilike(f'%{search}%') |
            LocalEvent.description.ilike(f'%{search}%')
        )
    
    if category:
        local_query = local_query.filter_by(category=category)
    
    local_events = local_query.order_by(LocalEvent.date.desc()).limit(per_page // 2).all()
    local_events_data = [
        {**event.to_dict(), 'source': 'local'}
        for event in local_events
    ]
    
    # Fetch Eventbrite events
    eventbrite_result = eventbrite_service.search_events(
        location=location,
        category=category,
        page=1,
        per_page=per_page // 2
    )
    eventbrite_events = eventbrite_result['events']
    
    # Merge and sort by date
    all_events = local_events_data + eventbrite_events
    all_events.sort(key=lambda x: x.get('date', ''), reverse=True)
    
    # Paginate
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_events = all_events[start_idx:end_idx]
    
    total_pages = (len(all_events) + per_page - 1) // per_page
    
    return jsonify({
        'events': paginated_events,
        'total_pages': total_pages,
        'current_page': page,
        'total_events': len(all_events),
        'local_count': len(local_events_data),
        'eventbrite_count': len(eventbrite_events)
    })
