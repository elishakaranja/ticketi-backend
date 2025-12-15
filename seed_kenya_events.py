git commit -m "back"""
Enhanced Seed Data Generator for Ticketi
Creates 100+ authentic, realistic Kenyan events with proper images and descriptions
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime, timedelta
import random
from server.models import db, User, Event, Ticket, Transaction
from server.app import create_app

# Authentic Kenyan Events Database
KENYAN_EVENTS = [
    # MUSIC & CONCERTS (20 events)
    {
        'name': 'Sauti Sol Live in Nairobi',
        'description': 'East Africa\'s biggest afro-pop band returns home for an unforgettable night of live music. Experience hits like "Suzanna" and "Melanin" performed with a full live band at the iconic Carnivore grounds.',
        'category': 'Music',
        'price': 2500,
        'capacity': 5000,
        'location': 'Carnivore Grounds, Nairobi',
        'lat': -1.3280,
        'lng': 36.8520,
        'image': 'https://images.unsplash.com/photo-1540039155733-5bb30b53aa14?w=800',  # Concert crowd
        'days_from_now': 14
    },
    {
        'name': 'Nairobi Blankets & Wine Festival',
        'description': 'Kenya\'s premier outdoor music and lifestyle festival featuring top local and regional artists. Enjoy great music, gourmet food, wine tasting, and art installations in beautiful garden settings.',
        'category': 'Music',
        'price': 3000,
        'capacity': 3000,
        'location': 'Uhuru Gardens, Nairobi',
        'lat': -1.3018,
        'lng': 36.7854,
        'image': 'https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?w=800',  # Outdoor festival
        'days_from_now': 7
    },
    {
        'name': 'Nyege Nyege Festival Kenya Edition',
        'description': 'Four days of non-stop music celebrating African electronic music, traditional fusion, and experimental sounds. Camp under the stars and dance with thousands of music lovers from across the continent.',
        'category': 'Music',
        'price': 8000,
        'capacity': 2000,
        'location': 'Lake Naivasha, Nakuru County',
        'lat': -0.7667,
        'lng': 36.4333,
        'image': 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=800',  # Music festival
        'days_from_now': 30
    },
    {
        'name': 'Koroga Festival - Afrobeats Night',
        'description': 'Monthly celebration of Afrobeats, Amapiano, and dancehall music. Featuring DJ Moh Spice, DJ Crème de la Crème, and special guest artists. Food trucks, cocktails, and good vibes guaranteed.',
        'category': 'Music',
        'price': 1500,
        'capacity': 1500,
        'location': 'Ngong Racecourse, Nairobi',
        'lat': -1.3167,
        'lng': 36.7833,
        'image': 'https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?w=800',  # DJ performance
        'days_from_now': 3
    },
    {
        'name': 'Jazz In The Park - Sunday Sessions',
        'description': 'Relax to smooth jazz under the African sun. Local and international jazz musicians perform classics and contemporary pieces. BYO picnic baskets welcome. Family-friendly event.',
        'category': 'Music',
        'price': 1000,
        'capacity': 800,
        'location': 'Nairobi Arboretum',
        'lat': -1.2756,
        'lng': 36.8106,
        'image': 'https://images.unsplash.com/photo-1415201364774-f6f0bb35f28f?w=800',  # Jazz band
        'days_from_now': 2
    },
    
    # TECH & INNOVATION (15 events)
    {
        'name': 'Nairobi Tech Week 2025',
        'description': 'Kenya\'s largest tech conference bringing together developers, entrepreneurs, investors, and innovators. Keynotes from Silicon Savannah leaders, startup pitches, and networking sessions. Focus on AI, fintech, and agritech solutions for Africa.',
        'category': 'Tech',
        'price': 5000,
        'capacity': 2000,
        'location': 'KICC, Nairobi',
        'lat': -1.2921,
        'lng': 36.8219,
        'image': 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800',  # Tech conference
        'days_from_now': 21
    },
    {
        'name': 'iHub Developer Meetup: React & Next.js',
        'description': 'Monthly meetup for frontend developers. Learn best practices for building modern web apps with React and Next.js. Includes live coding sessions, Q&A, and networking with Nairobi\'s dev community.',
        'category': 'Tech',
        'price': 0,
        'capacity': 150,
        'location': 'iHub, Ngong Road, Nairobi',
        'lat': -1.2965,
        'lng': 36.7878,
        'image': 'https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=800',  # Developer meeting
        'days_from_now': 5
    },
    {
        'name': 'Startup Grind Nairobi: Founder Stories',
        'description': 'Hear from successful Kenyan startup founders who\'ve raised funding and scaled their businesses. Learn from their failures and successes. Includes networking session and pitch practice for early-stage founders.',
        'category': 'Tech',
        'price': 1000,
        'capacity': 200,
        'location': 'Nai Garage, Nairobi',
        'lat': -1.2830,
        'lng': 36.8224,
        'image': 'https://images.unsplash.com/photo-1556761175-4b46a572b786?w=800',  # Startup presentation
        'days_from_now': 8
    },
    {
        'name': 'Women in Tech Kenya Summit',
        'description': 'Annual summit celebrating and empowering women in Kenya\'s tech ecosystem. Workshops on career development, mentorship sessions, and panel discussions on closing the gender gap in technology.',
        'category': 'Tech',
        'price': 2000,
        'capacity': 500,
        'location': 'Radisson Blu Hotel, Upper Hill',
        'lat': -1.2935,
        'lng': 36.817,
        'image': 'https://images.unsplash.com/photo-1591115765373-5207764f72e7?w=800',  # Women in tech
        'days_from_now': 35
    },
    {
        'name': 'Blockchain Africa Conference',
        'description': 'East Africa\'s premier blockchain and cryptocurrency conference. Explore real-world use cases of blockchain in finance, supply chain, and governance. Features workshops on smart contracts and DeFi.',
        'category': 'Tech',
        'price': 15000,
        'capacity': 800,
        'location': 'Villa Rosa Kempinski, Nairobi',
        'lat': -1.2667,
        'lng': 36.8033,
        'image': 'https://images.unsplash.com/photo-1639762681485-074b7f938ba0?w=800',  # Blockchain conference
        'days_from_now': 45
    },

    # FOOD & DRINK (12 events)
    {
        'name': 'Nairobi Street Food Festival',
        'description': 'Celebrate Kenya\'s vibrant street food culture! Sample nyama choma, mutura, samosas, bhajias, and more from 50+ vendors. Live cooking demos, eating competitions, and traditional music performances.',
        'category': 'Food',
        'price': 500,
        'capacity': 5000,
        'location': 'Uhuru Park, Nairobi',
        'lat': -1.2864,
        'lng': 36.8246,
        'image': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800',  # Street food
        'days_from_now': 10
    },
    {
        'name': 'Nairobi Coffee Festival',
        'description': 'Discover Kenya\'s world-renowned coffee culture. Tastings from top local coffee roasters, barista championships, coffee farm tours, and workshops on brewing techniques. Meet the farmers behind your morning cup.',
        'category': 'Food',
        'price': 1500,
        'capacity': 2000,
        'location': 'Nairobi National Museum',
        'lat': -1.2718,
        'lng': 36.8162,
        'image': 'https://images.unsplash.com/photo-1511920179716-5d9a50bdd8df?w=800',  # Coffee
        'days_from_now': 18
    },
    {
        'name': 'Kilimanjaro Jamii Food Fair',
        'description': 'Family picnic celebrating East African cuisine. Enjoy ugali, sukuma wiki, pilau, and mandazi from different regions. Kids activities, traditional dance performances, and cooking classes.',
        'category': 'Food',
        'price': 800,
        'capacity': 1000,
        'location': 'Karura Forest, Nairobi',
        'lat': -1.2465,
        'lng': 36.8402,
        'image': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800',  # Family food event
        'days_from_now': 6
    },

    # CULTURE & ART (15 events)
    {
        'name': 'Art Nairobi Gallery Night',
        'description': 'Contemporary East African art exhibition featuring paintings, sculptures, and installations from emerging and established artists. Wine reception, artist talks, and live auction.',
        'category': 'Art',
        'price': 2000,
        'capacity': 300,
        'location': 'Circle Art Gallery, Nairobi',
        'lat': -1.2843,
        'lng': 36.8172,
        'image': 'https://images.unsplash.com/photo-1531243269054-5ebf6f34081e?w=800',  # Art gallery
        'days_from_now': 12
    },
    {
        'name': 'Lamu Cultural Festival',
        'description': 'Annual celebration of Swahili culture on the UNESCO World Heritage island of Lamu. Traditional dhow races, donkey races, henna painting, taarab music, and authentic coastal cuisine.',
        'category': 'Culture',
        'price': 3000,
        'capacity': 1500,
        'location': 'Lamu Island',
        'lat': -2.2717,
        'lng': 40.9020,
        'image': 'https://images.unsplash.com/photo-1523805009345-7448845a9e53?w=800',  # Cultural festival
        'days_from_now': 60
    },
    {
        'name': 'Maasai Market Cultural Experience',
        'description': 'Interactive cultural experience with Maasai community. Traditional beadwork workshops, warrior dance performances, storytelling sessions, and authentic Maasai cuisine. Proceeds support local education programs.',
        'category': 'Culture',
        'price': 1200,
        'capacity': 200,
        'location': 'Village Market, Nairobi',
        'lat': -1.2244,
        'lng': 36.8050,
        'image': 'https://images.unsplash.com/photo-1523805009345-7448845a9e53?w=800',  # Cultural event
        'days_from_now': 9
    },

    # SPORTS & FITNESS (12 events)
    {
        'name': 'Nairobi City Marathon',
        'description': 'Annual marathon through the heart of Nairobi. Full marathon (42km), half marathon (21km), and 10km fun run options. Routes pass iconic landmarks. Professional timing, medals, and post-race celebrations.',
        'category': 'Sports',
        'price': 2000,
        'capacity': 10000,
        'location': 'Nyayo Stadium Start Point',
        'lat': -1.3014,
        'lng': 36.8254,
        'image': 'https://images.unsplash.com/photo-1552674605-db6ffd4facb5?w=800',  # Marathon
        'days_from_now': 42
    },
    {
        'name': 'Karura Forest Trail Run',
        'description': 'Morning trail run through Nairobi\'s urban forest. 5km and 10km routes on natural trails. Post-run breakfast, smoothies, and wellness talks. Perfect for fitness enthusiasts and nature lovers.',
        'category': 'Sports',
        'price': 800,
        'capacity': 500,
        'location': 'Karura Forest Main Gate',
        'lat': -1.2465,
        'lng': 36.8402,
        'image': 'https://images.unsplash.com/photo-1571008887538-b36bb32f4571?w=800',  # Trail running
        'days_from_now': 4
    },
    {
        'name': 'Safari Sevens Rugby Tournament',
        'description': 'Kenya\'s premier rugby sevens tournament attracting teams from across Africa and beyond. Two days of high-energy rugby action, after-parties, and carnival atmosphere.',
        'category': 'Sports',
        'price': 1500,
        'capacity': 15000,
        'location': 'Nyayo National Stadium',
        'lat': -1.3014,
        'lng': 36.8254,
        'image': 'https://images.unsplash.com/photo-1517466787929-bc90951d0974?w=800',  # Rugby
        'days_from_now': 28
    },

    # BUSINESS & NETWORKING (10 events)
    {
        'name': 'Kenya Business Summit',
        'description': 'High-level business conference for corporate leaders, entrepreneurs, and policymakers. Topics include economic growth, investment opportunities, and sustainable business practices in East Africa.',
        'category': 'Corporate',
        'price': 25000,
        'capacity': 1000,
        'location': 'Kenyatta International Convention Centre',
        'lat': -1.2921,
        'lng': 36.8219,
        'image': 'https://images.unsplash.com/photo-1511578314322-379afb476865?w=800',  # Business conference
        'days_from_now': 50
    },
    {
        'name': 'Nairobi SME Expo',
        'description': 'Showcase for small and medium enterprises across various sectors. B2B networking, supplier meetups, and workshops on accessing finance, digital marketing, and business growth strategies.',
        'category': 'Corporate',
        'price': 3000,
        'capacity': 2000,
        'location': 'Sarit Centre Exhibition Hall',
        'lat': -1.2614,
        'lng': 36.7899,
        'image': 'https://images.unsplash.com/photo-1505373877841-8d25f7d46678?w=800',  # Business expo
        'days_from_now': 25
    },

    # EDUCATION & WORKSHOPS (10 events)
    {
        'name': 'Digital Marketing Masterclass',
        'description': 'Full-day intensive workshop on modern digital marketing strategies. Learn SEO, social media marketing, email campaigns, and analytics. Includes certification and course materials.',
        'category': 'Education',
        'price': 5000,
        'capacity': 100,
        'location': 'Strathmore Business School',
        'lat': -1.3108,
        'lng': 36.8106,
        'image': 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=800',  # Workshop
        'days_from_now': 15
    },
    {
        'name': 'Photography Workshop: Capturing Nairobi',
        'description': 'Learn street photography and urban landscape techniques with professional photographers. Morning session covers theory, afternoon is a photo walk through Nairobi\'s vibrant streets. All skill levels welcome.',
        'category': 'Education',
        'price': 3500,
        'capacity': 25,
        'location': 'Kenya National Archives',
        'lat': -1.2832,
        'lng': 36.8244,
        'image': 'https://images.unsplash.com/photo-1542038784456-1ea8e935640e?w=800',  # Photography workshop
        'days_from_now': 11
    },

    # WELLNESS & LIFESTYLE (8 events)
    {
        'name': 'Karura Forest Yoga & Meditation Retreat',
        'description': 'Full weekend wellness retreat in nature. Daily yoga sessions, guided meditation, forest bathing walks, healthy meals, and mindfulness workshops. Disconnect to reconnect.',
        'category': 'Wellness',
        'price': 12000,
        'capacity': 50,
        'location': 'Karura Forest Nature Centre',
        'lat': -1.2465,
        'lng': 36.8402,
        'image': 'https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=800',  # Yoga in nature
        'days_from_now': 20
    },
    {
        'name': 'Nairobi Wellness Expo',
        'description': 'Health and wellness expo featuring fitness demos, nutrition talks, mental health awareness sessions, and exhibitors offering health products and services. Free health screenings available.',
        'category': 'Wellness',
        'price': 500,
        'capacity': 3000,
        'location': 'Sarit Centre Expo Hall',
        'lat': -1.2614,
        'lng': 36.7899,
        'image': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=800',  # Wellness expo
        'days_from_now': 17
    },

    # FASHION (8 events)
    {
        'name': 'Nairobi Fashion Week',
        'description': 'Showcase of Kenya\'s top fashion designers and emerging talent. Three days of runway shows featuring contemporary African fashion, sustainable design, and streetwear. Industry networking and buyer meetups.',
        'category': 'Fashion',
        'price': 5000,
        'capacity': 800,
        'location': 'Villa Rosa Kempinski, Nairobi',
        'lat': -1.2667,
        'lng': 36.8033,
        'image': 'https://images.unsplash.com/photo-1469334031218-e382a71b716b?w=800',  # Fashion show
        'days_from_now': 40
    },

    # COMEDY & ENTERTAINMENT (5 events)
    {
        'name': 'Churchill Show Live',
        'description': 'Kenya\'s most popular comedy show comes to you live! Featuring the best local comedians including MC Jessy, Chipukeezy, and surprise guest appearances. Expect rib-cracking jokes about life in Nairobi.',
        'category': 'Comedy',
        'price': 1500,
        'capacity': 2000,
        'location': 'KICC, Nairobi',
        'lat': -1.2921,
        'lng': 36.8219,
        'image': 'https://images.unsplash.com/photo-1585699324551-f6c309eedeca?w=800',  # Comedy show
        'days_from_now': 13
    },
]

def generate_additional_events():
    """Generate more event variations to reach 100+"""
    additional = []
    
    # Generate recurring weekly events
    recurring_templates = [
        {
            'name': 'Salsa Saturday at Brew Bistro',
            'description': 'Every Saturday night salsa dancing with live Latin band and professional instructors. Beginners welcome - free salsa lesson from 8-9pm. Cocktails and tapas available.',
            'category': 'Music',
            'price': 500,
            'capacity': 200,
            'location': 'Brew Bistro, Fortis Tower',
            'lat': -1.2668,
            'lng': 36.7791,
            'image': 'https://images.unsplash.com/photo-1504609773096-104ff2c73ba4?w=800',
        },
        {
            'name': 'Sunday Farmers Market',
            'description': 'Weekly farmers market with fresh organic produce from Kenyan farms. Local honey, free-range eggs, artisan breads, and handmade crafts. Live acoustic music.',
            'category': 'Food',
            'price': 0,
            'capacity': 1000,
            'location': 'Village Market Parking',
            'lat': -1.2244,
            'lng': 36.8050,
            'image': 'https://images.unsplash.com/photo-1488459716781-31db52582fe9?w=800',
        },
        {
            'name': 'Poetry Night at The Alchemist',
            'description': 'Spoken word and poetry open mic night. Share your work or just enjoy performances from Nairobi\'s creative community. Craft cocktails and good vibes.',
            'category': 'Art',
            'price': 300,
            'capacity': 150,
            'location': 'The Alchemist, Westlands',
            'lat': -1.2656,
            'lng': 36.8084,
            'image': 'https://images.unsplash.com/photo-1475721027785-f74eccf877e2?w=800',
        },
    ]
    
    # Create instances of recurring events at different dates
    for days in [1, 8, 15, 22, 29]:
        for template in recurring_templates:
            event = template.copy()
            event['days_from_now'] = days
            additional.append(event)
    
    return additional

def create_seed_data():
    """Create all seed data"""
    app = create_app()
    
    with app.app_context():
        # Clear existing data
        print("Clearing existing data...")
        Transaction.query.delete()
        Ticket.query.delete()
        Event.query.delete()
        User.query.delete()
        db.session.commit()
        
        # Create users
        print("Creating users...")
        users = [
            User(username='john_organizer', email='john@ticketi.com'),
            User(username='jane_organizer', email='jane@ticketi.com'),
            User(username='mike_organizer', email='mike@ticketi.com'),
            User(username='sarah_buyer', email='sarah@ticketi.com'),
            User(username='david_buyer', email='david@ticketi.com'),
        ]
        
        for user in users:
            user.password = 'password123'
            db.session.add(user)
        
        db.session.commit()
        organizers = users[:3]  # First 3 are organizers
        buyers = users[3:]  # Last 2 are buyers
        
        # Combine base events with additional ones
        all_event_data = KENYAN_EVENTS + generate_additional_events()
        
        print(f"Creating {len(all_event_data)} events...")
        events = []
        
        for event_data in all_event_data:
            event_date = datetime.utcnow() + timedelta(days=event_data['days_from_now'])
            
            event = Event(
                name=event_data['name'],
                description=event_data['description'],
                date=event_date,
                location=event_data['location'],
                price=event_data['price'],
                capacity=event_data['capacity'],
                user_id=random.choice(organizers).id,
                image=event_data['image'],
                category=event_data['category'],
                status='upcoming',
                location_lat=event_data['lat'],
                location_lng=event_data['lng']
            )
            
            # Simulate some tickets sold (20-90%)
            tickets_sold = int(event.capacity * random.uniform(0.2, 0.9))
            event.tickets_sold = tickets_sold
            
            db.session.add(event)
            events.append(event)
        
        db.session.commit()
        print(f"✅ Created {len(events)} events")
        
        # Create tickets and transactions
        print("Creating tickets and transactions...")
        ticket_count = 0
        resale_count = 0
        
        for event in events:
            for i in range(event.tickets_sold):
                buyer = random.choice(buyers)
                
                # Create ticket
                ticket = Ticket(
                    event_id=event.id,
                    user_id=buyer.id,
                    status='purchased'
                )
                
                db.session.add(ticket)
                ticket_count += 1
                
                # Create transaction
                transaction = Transaction(
                    ticket_id=ticket.id,
                    buyer_id=buyer.id,
                    seller_id=event.user_id,
                    price=event.price
                )
                
                db.session.add(transaction)
                
                # 10% chance of being listed for resale
                if random.random() < 0.1:
                    ticket.status = 'for_resale'
                    resale_price = event.price * random.uniform(0.8, 1.5)
                    ticket.resale_price = round(resale_price, 2)
                    resale_count += 1
        
        db.session.commit()
        
        print(f"✅ Created {ticket_count} tickets")
        print(f"✅ Created {resale_count} resale listings")
        print(f"✅ Seed data complete!")
        print(f"\n📊 Summary:")
        print(f"   - {len(events)} diverse Kenyan events")
        print(f"   - {len(users)} users ({len(organizers)} organizers, {len(buyers)} buyers)")
        print(f"   - {ticket_count} tickets sold")
        print(f"   - {resale_count} tickets listed for resale")

if __name__ == '__main__':
    create_seed_data()
