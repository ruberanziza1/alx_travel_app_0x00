from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from listings.models import Listing, Booking, Review
from decimal import Decimal
from datetime import date, timedelta
import random

class Command(BaseCommand):
    help = 'Seed the database with sample listings, bookings, and reviews data'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=10,
            help='Number of users to create (default: 10)'
        )
        parser.add_argument(
            '--listings',
            type=int,
            default=20,
            help='Number of listings to create (default: 20)'
        )
        parser.add_argument(
            '--bookings',
            type=int,
            default=30,
            help='Number of bookings to create (default: 30)'
        )
        parser.add_argument(
            '--reviews',
            type=int,
            default=25,
            help='Number of reviews to create (default: 25)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding'
        )
    
    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            Review.objects.all().delete()
            Booking.objects.all().delete()
            Listing.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write(self.style.SUCCESS('Data cleared successfully!'))
        
        # Create users
        self.stdout.write('Creating users...')
        users = self.create_users(options['users'])
        self.stdout.write(
            self.style.SUCCESS(f'Created {len(users)} users')
        )
        
        # Create listings
        self.stdout.write('Creating listings...')
        listings = self.create_listings(users, options['listings'])
        self.stdout.write(
            self.style.SUCCESS(f'Created {len(listings)} listings')
        )
        
        # Create bookings
        self.stdout.write('Creating bookings...')
        bookings = self.create_bookings(users, listings, options['bookings'])
        self.stdout.write(
            self.style.SUCCESS(f'Created {len(bookings)} bookings')
        )
        
        # Create reviews
        self.stdout.write('Creating reviews...')
        reviews = self.create_reviews(users, listings, options['reviews'])
        self.stdout.write(
            self.style.SUCCESS(f'Created {len(reviews)} reviews')
        )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSeeding completed successfully!\n'
                f'Users: {len(users)}\n'
                f'Listings: {len(listings)}\n'
                f'Bookings: {len(bookings)}\n'
                f'Reviews: {len(reviews)}'
            )
        )
    
    def create_users(self, count):
        """Create sample users"""
        users = []
        first_names = ['John', 'Jane', 'Mike', 'Sarah', 'David', 'Emma', 'Chris', 'Lisa', 'Tom', 'Anna']
        last_names = ['Smith', 'Johnson', 'Brown', 'Davis', 'Wilson', 'Miller', 'Moore', 'Taylor', 'Anderson', 'Thomas']
        
        for i in range(count):
            username = f'user_{i+1}'
            email = f'user{i+1}@example.com'
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                }
            )
            if created:
                user.set_password('password123')
                user.save()
            users.append(user)
        
        return users
    
    def create_listings(self, users, count):
        """Create sample listings"""
        listings = []
        
        # Sample data
        cities = [
            'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
            'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose',
            'Austin', 'Jacksonville', 'Fort Worth', 'Columbus', 'Charlotte'
        ]
        
        property_types = [
            'Cozy Apartment', 'Modern Condo', 'Spacious House', 'Luxury Villa',
            'Studio Loft', 'Beach House', 'Mountain Cabin', 'City Penthouse',
            'Garden Cottage', 'Downtown Flat'
        ]
        
        descriptions = [
            'Beautiful and comfortable accommodation with all amenities.',
            'Perfect location with easy access to attractions and transport.',
            'Fully equipped with modern facilities and stunning views.',
            'Ideal for families and groups looking for a memorable stay.',
            'Charming property with unique character and style.',
            'Recently renovated with high-end finishes and appliances.',
            'Peaceful retreat away from the hustle and bustle.',
            'Convenient location near restaurants, shops, and entertainment.',
            'Spacious and bright with plenty of natural light.',
            'Comfortable and clean with all the essentials provided.'
        ]
        
        for i in range(count):
            host = random.choice(users)
            city = random.choice(cities)
            property_type = random.choice(property_types)
            
            title = f"{property_type} in {city}"
            description = random.choice(descriptions)
            location = f"{city}, {random.choice(['NY', 'CA', 'TX', 'FL', 'IL'])}"
            price_per_night = Decimal(random.randint(50, 500))
            bedrooms = random.randint(1, 4)
            bathrooms = random.randint(1, 3)
            max_guests = bedrooms * 2
            
            # Available dates (next 6 months)
            available_from = date.today() + timedelta(days=random.randint(1, 30))
            available_to = available_from + timedelta(days=random.randint(90, 180))
            
            listing = Listing.objects.create(
                host=host,
                title=title,
                description=description,
                location=location,
                price_per_night=price_per_night,
                bedrooms=bedrooms,
                bathrooms=bathrooms,
                max_guests=max_guests,
                available_from=available_from,
                available_to=available_to
            )
            listings.append(listing)
        
        return listings
    
    def create_bookings(self, users, listings, count):
        """Create sample bookings"""
        bookings = []
        statuses = ['pending', 'confirmed', 'canceled', 'completed']
        
        for i in range(count):
            guest = random.choice(users)
            listing = random.choice(listings)
            
            # Ensure guest is not the host
            while guest == listing.host:
                guest = random.choice(users)
            
            # Random booking dates within availability
            days_from_available = random.randint(0, 60)
            check_in_date = listing.available_from + timedelta(days=days_from_available)
            duration = random.randint(1, 14)  # 1-14 days
            check_out_date = check_in_date + timedelta(days=duration)
            
            # Ensure booking is within availability period
            if check_out_date > listing.available_to:
                continue
            
            number_of_guests = random.randint(1, listing.max_guests)
            total_price = listing.price_per_night * duration
            status = random.choice(statuses)
            
            try:
                booking = Booking.objects.create(
                    listing=listing,
                    guest=guest,
                    check_in_date=check_in_date,
                    check_out_date=check_out_date,
                    number_of_guests=number_of_guests,
                    total_price=total_price,
                    status=status
                )
                bookings.append(booking)
            except Exception as e:
                # Skip if there's a constraint violation
                continue
        
        return bookings
    
    def create_reviews(self, users, listings, count):
        """Create sample reviews"""
        reviews = []
        comments = [
            'Amazing place! Highly recommend to anyone visiting the area.',
            'Clean, comfortable, and exactly as described. Great host!',
            'Perfect location and beautiful property. Will definitely stay again.',
            'Good value for money. Host was very responsive and helpful.',
            'Nice place but could use some updates. Overall satisfied.',
            'Exceeded expectations! Everything was perfect.',
            'Cozy and comfortable. Felt like home away from home.',
            'Great amenities and stunning views. Loved our stay!',
            'Host was wonderful and the place was spotless.',
            'Convenient location with easy access to everything we needed.',
            'Beautiful property with all the essentials. Highly recommended!',
            'Had a wonderful time. The place was exactly as advertised.',
            'Clean, safe, and comfortable. Perfect for our trip.',
            'Outstanding hospitality and attention to detail.',
            'Would definitely book again. Five stars!'
        ]
        
        created_reviews = 0
        attempts = 0
        max_attempts = count * 3  # Prevent infinite loop
        
        while created_reviews < count and attempts < max_attempts:
            attempts += 1
            guest = random.choice(users)
            listing = random.choice(listings)
            
            # Ensure guest is not the host and hasn't reviewed this listing
            if (guest == listing.host or 
                Review.objects.filter(guest=guest, listing=listing).exists()):
                continue
            
            rating = random.choices(
                [1, 2, 3, 4, 5],
                weights=[2, 3, 10, 30, 55]  # Bias towards higher ratings
            )[0]
            comment = random.choice(comments)
            
            try:
                review = Review.objects.create(
                    listing=listing,
                    guest=guest,
                    rating=rating,
                    comment=comment
                )
                reviews.append(review)
                created_reviews += 1
            except Exception as e:
                # Skip if there's a constraint violation
                continue
        
        return reviews
