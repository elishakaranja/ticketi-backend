"""
Eventbrite API Service for Ticketi
Fetches real events from Eventbrite with focus on Kenya/Nairobi
"""

import os
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class EventbriteService:
    """Service for fetching events from Eventbrite API"""
    
    BASE_URL = "https://www.eventbriteapi.com/v3"
    
    def __init__(self):
        self.api_key = os.getenv('EVENTBRITE_API_KEY')
        if not self.api_key:
            print("Warning: EVENTBRITE_API_KEY not set in environment")
        
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
    
    # Category mapping: Eventbrite -> Ticketi
    CATEGORY_MAP = {
        'music': 'Music',
        'business': 'Tech',
        'food-and-drink': 'Food',
        'health': 'Wellness',
        'sports-and-fitness': 'Sports',
        'travel-and-outdoor': 'Culture',
        'charity-and-causes': 'Culture',
        'community': 'Culture',
        'family-and-education': 'Education',
        'fashion': 'Fashion',
        'film-and-media': 'Film',
        'hobbies': 'Culture',
        'home-and-lifestyle': 'Culture',
        'performing-arts': 'Art',
        'religion-and-spirituality': 'Culture',
        'school-activities': 'Education',
        'science-and-tech': 'Tech',
        'seasonal': 'Culture',
        'other': 'Culture'
    }
    
    def search_events(
        self,
        location: str = "Nairobi, Kenya",
        category: Optional[str] = None,
        page: int = 1,
        per_page: int = 20,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict:
        """
        Search for events on Eventbrite
        
        Args:
            location: Location string (default: Nairobi, Kenya)
            category: Event category filter
            page: Page number for pagination
            per_page: Results per page (max 50)
            start_date: Filter events starting from this date (YYYY-MM-DD)
            end_date: Filter events ending before this date (YYYY-MM-DD)
        
        Returns:
            Dict with 'events' list and 'pagination' info
        """
        if not self.api_key:
            return {'events': [], 'pagination': {'page_count': 0}}
        
        url = f"{self.BASE_URL}/events/search/"
        
        params = {
            'location.address': location,
            'location.within': '50km',  # Search within 50km of location
            'expand': 'venue,ticket_availability,category',
            'page': page,
            'page_size': min(per_page, 50)  # Eventbrite max is 50
        }
        
        # Add date filters
        if start_date:
            params['start_date.range_start'] = f"{start_date}T00:00:00Z"
        
        if end_date:
            params['start_date.range_end'] = f"{end_date}T23:59:59Z"
        
        # Add category filter (map from our categories to Eventbrite)
        if category:
            eventbrite_category = self._get_eventbrite_category(category)
            if eventbrite_category:
                params['categories'] = eventbrite_category
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Transform events to our format
            events = [self._transform_event(event) for event in data.get('events', [])]
            
            return {
                'events': events,
                'pagination': data.get('pagination', {})
            }
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching Eventbrite events: {e}")
            return {'events': [], 'pagination': {'page_count': 0}}
    
    def get_events_near_location(
        self,
        latitude: float,
        longitude: float,
        radius_km: int = 25,
        category: Optional[str] = None,
        limit: int = 20
    ) -> List[Dict]:
        """
        Get events near a specific lat/lng coordinate
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            radius_km: Search radius in kilometers
            category: Optional category filter
            limit: Maximum number of results
        
        Returns:
            List of transformed events
        """
        if not self.api_key:
            return []
        
        url = f"{self.BASE_URL}/events/search/"
        
        params = {
            'location.latitude': latitude,
            'location.longitude': longitude,
            'location.within': f'{radius_km}km',
            'expand': 'venue,ticket_availability,category',
            'page_size': min(limit, 50)
        }
        
        if category:
            eventbrite_category = self._get_eventbrite_category(category)
            if eventbrite_category:
                params['categories'] = eventbrite_category
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            events = [self._transform_event(event) for event in data.get('events', [])]
            
            return events
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching nearby events: {e}")
            return []
    
    def _transform_event(self, eventbrite_event: Dict) -> Dict:
        """Transform Eventbrite event to our format"""
        
        # Extract basic info
        event_id = eventbrite_event.get('id', '')
        name = eventbrite_event.get('name', {}).get('text', 'Untitled Event')
        description = eventbrite_event.get('description', {}).get('text', '')[:500]  # Truncate
        
        # Parse dates
        start_date = eventbrite_event.get('start', {}).get('utc', '')
        if start_date:
            try:
                date_obj = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                date_str = date_obj.strftime('%Y-%m-%d %H:%M:%S')
            except:
                date_str = start_date
        else:
            date_str = datetime.utcnow().isoformat()
        
        # Extract venue info
        venue = eventbrite_event.get('venue', {})
        location = venue.get('name', 'Online Event')
        if venue.get('address'):
            city = venue['address'].get('city', '')
            if city:
                location = f"{location}, {city}"
        
        location_lat = None
        location_lng = None
        if venue.get('latitude'):
            location_lat = float(venue['latitude'])
        if venue.get('longitude'):
            location_lng = float(venue['longitude'])
        
        # Get pricing
        ticket_availability = eventbrite_event.get('ticket_availability', {})
        is_free = eventbrite_event.get('is_free', True)
        
        if is_free:
            price = 0.0
        else:
            # Try to get minimum ticket price
            # Note: Full ticket pricing requires additional API calls
            price = 1000.0  # Default placeholder
        
        # Get capacity
        capacity = eventbrite_event.get('capacity', 100)
        
        # Calculate tickets sold (estimate from availability)
        tickets_sold = 0
        if ticket_availability.get('has_available_tickets') == False:
            tickets_sold = capacity
        
        # Get image
        logo = eventbrite_event.get('logo', {})
        image = logo.get('original', {}).get('url', '') if logo else ''
        
        # Map category
        category_obj = eventbrite_event.get('category', {})
        eventbrite_category = category_obj.get('short_name', '').lower() if category_obj else 'other'
        category = self.CATEGORY_MAP.get(eventbrite_category, 'Culture')
        
        # Event URL
        url = eventbrite_event.get('url', '')
        
        return {
            'id': f'eb_{event_id}',  # Prefix to distinguish from local events
            'name': name,
            'description': description,
            'date': date_str,
            'location': location,
            'location_lat': location_lat,
            'location_lng': location_lng,
            'price': price,
            'capacity': capacity,
            'tickets_sold': tickets_sold,
            'image': image,
            'category': category,
            'status': 'upcoming',
            'source': 'eventbrite',
            'external_url': url,
            'is_free': is_free
        }
    
    def _get_eventbrite_category(self, ticketi_category: str) -> Optional[str]:
        """Map our category to Eventbrite category ID"""
        # Reverse mapping
        reverse_map = {
            'Music': '103',
            'Tech': '102',
            'Food': '110',
            'Wellness': '107',
            'Sports': '108',
            'Culture': '113',
            'Fashion': '106',
            'Film': '104',
            'Art': '105',
            'Education': '114'
        }
        return reverse_map.get(ticketi_category)


# Singleton instance
eventbrite_service = EventbriteService()
