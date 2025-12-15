"""
Standalone seed script for Ticketi - works from project root
Run with: python -m server.seed_events
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from datetime import datetime, timedelta
from random import randint, choice

# Now import with server prefix
from app import create_app
from models import db, User, Event, Ticket, Transaction

# Kenyan event data with real locations
KENYAN_EVENTS = [
    {
        "name": "Nairobi Afrobeat Festival 2025",
        "description": "Experience three days of electrifying Afrobeat, Gengetone, and Amapiano performances featuring Kenya's hottest artists and international acts. Food vendors, art installations, and cultural showcases throughout.",
        "location": "Uhuru Gardens, Nairobi",
        "location_lat": -1.3142,
        "location_lng": 36.8194,
        "price": 2500.00,
        "capacity": 5000,
        "image": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=800",  # Outdoor music festival crowd
        "category": "Music",
        "date_offset": 45,  # days from now
        "tickets_to_sell": 450
    },
    {
        "name": "Tech Safari Summit Nairobi",
        "description": "East Africa's premier tech conference bringing together innovators, investors, and entrepreneurs. Keynotes from Silicon Savannah leaders, startup pitches, and networking sessions. Learn about AI, fintech, and agritech solutions shaping Kenya's future.",
        "location": "Kenyatta International Convention Centre (KICC), Nairobi",
        "location_lat": -1.2921,
        "location_lng": 36.8219,
        "price": 8500.00,
        "capacity": 800,
        "image": "https://images.unsplash.com/photo-1591115765373-5207764f72e7?w=800",  # Tech conference audience
        "category": "Tech",
        "date_offset": 30,
        "tickets_to_sell": 320
    },
    {
        "name": "Coastal Vibes: Mombasa Reggae Night",
        "description": "Beach sunset reggae session featuring local DJs and live bands. Chill vibes, ocean breeze, and authentic coastal cuisine. Special performance by Mombasa's finest reggae collective.",
        "location": "Nyali Beach, Mombasa",
        "location_lat": -4.0435,
        "location_lng": 39.7224,
        "price": 1500.00,
        "capacity": 300,
        "image": "https://images.unsplash.com/photo-1519046904884-53103b34b206?w=800",  # Beach sunset/coastal scene
        "category": "Music",
        "date_offset": 15,
        "tickets_to_sell": 120
    },
    {
        "name": "Nairobi Art Week: Contemporary East African Exhibition",
        "description": "Week-long celebration of contemporary art from Kenyan and East African artists. Gallery exhibitions, artist talks, live painting sessions, and art market. Explore the vibrant creative scene of Nairobi.",
        "location": "The Nairobi Gallery, Nairobi",
        "location_lat": -1.2864,
        "location_lng": 36.8172,
        "price": 1000.00,
        "capacity": 200,
        "image": "https://images.unsplash.com/photo-1531243625752-c0185649e1cf?w=800",  # Art gallery exhibition
        "category": "Art",
        "date_offset": 20,
        "tickets_to_sell": 85
    },
    {
        "name": "Karura Forest Wellness Retreat",
        "description": "Full-day wellness experience in Nairobi's urban forest. Yoga sessions, guided nature walks, meditation workshops, and healthy local cuisine. Reconnect with nature without leaving the city.",
        "location": "Karura Forest, Nairobi",
        "location_lat": -1.2503,
        "location_lng": 36.8345,
        "price": 3500.00,
        "capacity": 50,
        "image": "https://images.unsplash.com/photo-1545389336-cf090694435e?w=800",  # Forest/nature yoga
        "category": "Wellness",
        "date_offset": 12,
        "tickets_to_sell": 28
    },
    {
        "name": "Kisumu Jazz & Wine Festival",
        "description": "Lakeside jazz festival featuring smooth jazz, soul, and R&B performances. Wine tastings from local and international vineyards, gourmet food pairings, and sunset views over Lake Victoria.",
        "location": "Dunga Beach, Kisumu",
        "location_lat": -0.0917,
        "location_lng": 34.7680,
        "price": 4500.00,
        "capacity": 400,
        "image": "https://images.unsplash.com/photo-1415201364774-f6f0bb35f28f?w=800",  # Jazz performance
        "category": "Music",
        "date_offset": 60,
        "tickets_to_sell": 180
    },
    {
        "name": "Nairobi Street Food Festival",
        "description": "Celebrate Kenya's diverse culinary scene! Over 50 vendors serving everything from nyama choma to gourmet burgers, Swahili cuisine to international fusion. Live music, cooking demos, and eating competitions.",
        "location": "Museum Hill, Nairobi",
        "location_lat": -1.2693,
        "location_lng": 36.8122,
        "price": 800.00,
        "capacity": 3000,
        "image": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800",  # Street food/festival food
        "category": "Food",
        "date_offset": 8,
        "tickets_to_sell": 1200
    },
    {
        "name": "Startup Grind Nairobi: Pitching Masterclass",
        "description": "Learn from successful founders and investors. Interactive workshop on pitch deck creation, storytelling for fundraising, and navigating Kenya's startup ecosystem. Networking happy hour included.",
        "location": "iHub, Nairobi",
        "location_lat": -1.2897,
        "location_lng": 36.7836,
        "price": 2000.00,
        "capacity": 100,
        "image": "https://images.unsplash.com/photo-1552664730-d307ca884978?w=800",  # Business presentation/startup
        "category": "Tech",
        "date_offset": 18,
        "tickets_to_sell": 65
    },
    {
        "name": "Lamu Cultural Festival 2025",
        "description": "Annual celebration of Swahili culture and heritage. Traditional dhow races, donkey races, Swahili poetry, henna painting, and authentic coastal cuisine. Immerse yourself in centuries-old traditions.",
        "location": "Lamu Town, Lamu Island",
        "location_lat": -2.2717,
        "location_lng": 40.9020,
        "price": 6000.00,
        "capacity": 500,
        "image": "https://images.unsplash.com/photo-1568632234157-ce7aecd03d0d?w=800",  # Traditional African culture/festival
        "category": "Culture",
        "date_offset": 90,
        "tickets_to_sell": 220
    },
    {
        "name": "Nairobi Fashion Week: Emerging Designers Showcase",
        "description": "Runway shows featuring Kenya's next generation of fashion designers. Witness innovative designs blending traditional African aesthetics with contemporary fashion. VIP after-party with designers and industry leaders.",
        "location": "Sarit Centre, Nairobi",
        "location_lat": -1.2618,
        "location_lng": 36.7876,
        "price": 5000.00,
        "capacity": 250,
        "image": "https://images.unsplash.com/photo-1509631179647-0177331693ae?w=800",  # Fashion runway
        "category": "Fashion",
        "date_offset": 35,
        "tickets_to_sell": 140
    },
    {
        "name": "Rift Valley Marathon & Music Festival",
        "description": "Combine fitness and fun! Morning marathon through scenic Rift Valley landscapes, followed by afternoon music festival with local and regional artists. Family-friendly with kids' activities.",
        "location": "Lake Naivasha, Naivasha",
        "location_lat": -0.7667,
        "location_lng": 36.4333,
        "price": 3000.00,
        "capacity": 1000,
        "image": "https://images.unsplash.com/photo-1452626038306-9aae5e071dd3?w=800",  # Marathon/running
        "category": "Sports",
        "date_offset": 50,
        "tickets_to_sell": 420
    },
    {
        "name": "Nairobi Comedy Night: LOL Edition",
        "description": "Kenya's funniest stand-up comedians in one epic night! Featuring Churchill Show alumni and rising stars. Unlimited laughs, great food, and full bar. Adults only.",
        "location": "Kenya National Theatre, Nairobi",
        "location_lat": -1.2814,
        "location_lng": 36.8253,
        "price": 2000.00,
        "capacity": 400,
        "image": "https://images.unsplash.com/photo-1527224857830-43a7acc85260?w=800",  # Comedy/stand-up performance
        "category": "Comedy",
        "date_offset": 7,
        "tickets_to_sell": 310
    },
    {
        "name": "Blockchain & Crypto Summit Kenya",
        "description": "Explore the future of finance in Africa. Expert panels on cryptocurrency adoption, blockchain use cases for African challenges, NFTs, and DeFi. Networking with crypto enthusiasts and investors.",
        "location": "Villa Rosa Kempinski, Nairobi",
        "location_lat": -1.2674,
        "location_lng": 36.8075,
        "price": 12000.00,
        "capacity": 300,
        "image": "https://images.unsplash.com/photo-1620321023374-d1a68fbc720d?w=800",  # Crypto/blockchain conference
        "category": "Tech",
        "date_offset": 25,
        "tickets_to_sell": 180
    },
    {
        "name": "Kenyan Film Festival: New Voices",
        "description": "Week-long festival showcasing emerging Kenyan filmmakers. Feature films, documentaries, and shorts exploring contemporary Kenyan stories. Q&A sessions with directors and industry workshops.",
        "location": "Alliance Française, Nairobi",
        "location_lat": -1.2793,
        "location_lng": 36.8115,
        "price": 1500.00,
        "capacity": 150,
        "image": "https://images.unsplash.com/photo-1574267432644-f74c85cd023d?w=800",  # Cinema/film screening
        "category": "Film",
        "date_offset": 40,
        "tickets_to_sell": 95
    },
    {
        "name": "Nairobi Rooftop Sessions: Acoustic Sundown",
        "description": "Intimate acoustic performances on a stunning Nairobi rooftop. Local singer-songwriters, city skyline views, craft cocktails, and tapas. Limited capacity for exclusive experience.",
        "location": "Westlands, Nairobi",
        "location_lat": -1.2676,
        "location_lng": 36.8074,
        "price": 3500.00,
        "capacity": 80,
        "image": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800",  # Rooftop/cityscape evening
        "category": "Music",
        "date_offset": 10,
        "tickets_to_sell": 65
    },
    {
        "name": "Maasai Market Artisan Fair",
        "description": "Shop directly from Kenyan artisans! Handmade jewelry, textiles, leather goods, paintings, and sculptures. Live cultural performances, traditional food stalls, and meet-the-maker sessions.",
        "location": "Village Market, Nairobi",
        "location_lat": -1.2245,
        "location_lng": 36.8058,
        "price": 500.00,
        "capacity": 2000,
        "image": "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800",  # Artisan market/crafts
        "category": "Culture",
        "date_offset": 5,
        "tickets_to_sell": 850
    },
    {
        "name": "Nairobi Book Fair & Author Meet",
        "description": "Celebrate Kenyan literature! Book signings with bestselling Kenyan authors, poetry slams, writing workshops, and panel discussions on African storytelling. Discounted books and literary marketplace.",
        "location": "Sarit Expo Centre, Nairobi",
        "location_lat": -1.2618,
        "location_lng": 36.7876,
        "price": 1000.00,
        "capacity": 600,
        "image": "https://images.unsplash.com/photo-1457369804613-52c61a468e7d?w=800",  # Books/library/reading
        "category": "Literature",
        "date_offset": 28,
        "tickets_to_sell": 280
    },
    {
        "name": "Electronic Dance Music Festival Nairobi",
        "description": "Kenya's biggest EDM event! International and local DJs, massive light shows, multiple stages, VIP areas, and unforgettable vibes. Dance till dawn with thousands of music lovers.",
        "location": "Carnivore Grounds, Nairobi",
        "location_lat": -1.3439,
        "location_lng": 36.8361,
        "price": 4000.00,
        "capacity": 8000,
        "image": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=800",  # EDM/electronic music festival
        "category": "Music",
        "date_offset": 70,
        "tickets_to_sell": 3200
    }
]

def create_sample_users():
    """Create sample users as event organizers"""
    users = []
    
    user1 = User(
        username="sarahk",
        email="sarah@eventske.com",
        password="password123"
    )
    users.append(user1)
    
    user2 = User(
        username="davidm",
        email="david@nairobiEvents.com",
        password="password123"
    )
    users.append(user2)
    
    user3 = User(
        username="amina_organizer",
        email="amina@coastalevents.co.ke",
        password="password123"
    )
    users.append(user3)
    
    buyer1 = User(
        username="johndoe",
        email="john@example.com",
        password="password123"
    )
    users.append(buyer1)
    
    buyer2 = User(
        username="janedoe",
        email="jane@example.com",
        password="password123"
    )
    users.append(buyer2)
    
    return users

def seed_database():
    """Main seeding function"""
    app = create_app()
    
    with app.app_context():
        print("🌱 Starting database seeding...")
        
        # Check if already seeded
        existing_events = Event.query.count()
        if existing_events > 0:
            print(f"⚠️  Database already has {existing_events} events.")
            print("🗑️  Clearing existing data...")
            
            # Clear existing data
            Transaction.query.delete()
            Ticket.query.delete()
            Event.query.delete()
            User.query.delete()
            db.session.commit()
        
        # Create users
        print("👥 Creating sample users...")
        users = create_sample_users()
        for user in users:
            db.session.add(user)
        db.session.commit()
        print(f"✅ Created {len(users)} users")
        
        # Create events
        print("🎉 Creating Kenyan events...")
        today = datetime.utcnow()
        organizers = users[:3]  # First 3 users are organizers
        buyers = users[3:]  # Rest are buyers
        
        created_events = []
        for event_data in KENYAN_EVENTS:
            event_date = today + timedelta(days=event_data['date_offset'])
            
            event = Event(
                name=event_data['name'],
                description=event_data['description'],
                location=event_data['location'],
                location_lat=event_data['location_lat'],
                location_lng=event_data['location_lng'],
                price=event_data['price'],
                capacity=event_data['capacity'],
                image=event_data['image'],
                category=event_data['category'],
                date=event_date,
                status='upcoming' if event_date > today else 'completed',
                tickets_sold=event_data['tickets_to_sell'],
                user_id=choice(organizers).id
            )
            db.session.add(event)
            created_events.append((event, event_data['tickets_to_sell']))
        
        db.session.commit()
        print(f"✅ Created {len(KENYAN_EVENTS)} events")
        
        # Create tickets and transactions
        print("🎫 Creating sample tickets and transactions...")
        total_tickets = 0
        total_resale = 0
        
        for event, num_tickets in created_events:
            # Create sold tickets
            for i in range(num_tickets):
                buyer = choice(buyers)
                
                ticket = Ticket(
                    event_id=event.id,
                    user_id=buyer.id,
                    price=event.price,
                    status='sold',
                    purchase_date=datetime.utcnow() - timedelta(days=randint(1, 30))
                )
                db.session.add(ticket)
                
                # Create transaction for this ticket
                transaction = Transaction(
                    ticket_id=ticket.id,
                    seller_id=event.user_id,  # Event organizer as seller
                    buyer_id=buyer.id,
                    price=event.price,
                    transaction_type='primary',
                    status='completed',
                    timestamp=ticket.purchase_date
                )
                db.session.add(transaction)
                total_tickets += 1
                
                # 10% chance to put ticket up for resale
                if randint(1, 10) == 1:
                    ticket.status = 'resale'
                    # Resale price varies: 80% to 150% of original
                    ticket.resale_price = event.price * (0.8 + (randint(0, 70) / 100))
                    total_resale += 1
        
        db.session.commit()
        print(f"✅ Created {total_tickets} tickets ({total_resale} listed for resale)")
        
        # Print summary
        print("\n" + "="*50)
        print("🎊 DATABASE SEEDING COMPLETE!")
        print("="*50)
        print(f"👥 Users: {User.query.count()}")
        print(f"🎉 Events: {Event.query.count()}")
        print(f"🎫 Tickets: {Ticket.query.count()}")
        print(f"💰 Transactions: {Transaction.query.count()}")
        print(f"🔁 Resale Listings: {Ticket.query.filter_by(status='resale').count()}")
        print("\n📍 Event Categories:")
        for category in ['Music', 'Tech', 'Food', 'Art', 'Culture', 'Fashion', 'Sports', 'Comedy', 'Film', 'Literature', 'Wellness']:
            count = Event.query.filter_by(category=category).count()
            if count > 0:
                print(f"   {category}: {count}")
        print("\n✨ Ticketi is ready to showcase amazing Kenyan events!")
        print("="*50)

if __name__ == '__main__':
    seed_database()
