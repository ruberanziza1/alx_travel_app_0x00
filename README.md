# ALX Travel App 0x00

A Django REST API for a travel booking platform that allows users to create listings, make bookings, and leave reviews.

## Features

- **Listing Management**: Create and manage property listings
- **Booking System**: Book accommodations with validation
- **Review System**: Rate and review properties
- **User Management**: User authentication and profiles

## Models

### Listing
- **listing_id**: UUID primary key
- **host**: Foreign key to User
- **title**: Property title
- **description**: Detailed description
- **location**: Property location
- **price_per_night**: Decimal price
- **bedrooms**: Number of bedrooms
- **bathrooms**: Number of bathrooms
- **max_guests**: Maximum guest capacity
- **available_from/to**: Availability dates
- **created_at/updated_at**: Timestamps

### Booking
- **booking_id**: UUID primary key
- **listing**: Foreign key to Listing
- **guest**: Foreign key to User
- **check_in_date**: Check-in date
- **check_out_date**: Check-out date
- **number_of_guests**: Number of guests
- **total_price**: Total booking price
- **status**: Booking status (pending, confirmed, canceled, completed)
- **created_at/updated_at**: Timestamps

### Review
- **review_id**: UUID primary key
- **listing**: Foreign key to Listing
- **guest**: Foreign key to User
- **booking**: OneToOne to Booking (optional)
- **rating**: Integer rating (1-5)
- **comment**: Review text
- **created_at/updated_at**: Timestamps

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd alx_travel_app
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install django djangorestframework
   ```

4. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

## Database Seeding

The project includes a management command to populate the database with sample data.

### Run the seed command:
```bash
# Seed with default amounts
python manage.py seed

# Seed with custom amounts
python manage.py seed --users 20 --listings 50 --bookings 100 --reviews 80

# Clear existing data and seed
python manage.py seed --clear

# Help for all options
python manage.py seed --help
```

### Seed command options:
- `--users`: Number of users to create (default: 10)
- `--listings`: Number of listings to create (default: 20)
- `--bookings`: Number of bookings to create (default: 30)
- `--reviews`: Number of reviews to create (default: 25)
- `--clear`: Clear existing data before seeding

## API Endpoints

### Listings
- `GET /api/listings/` - List all listings
- `POST /api/listings/` - Create new listing
- `GET /api/listings/{id}/` - Get specific listing
- `PUT /api/listings/{id}/` - Update listing
- `DELETE /api/listings/{id}/` - Delete listing

### Bookings
- `GET /api/bookings/` - List user's bookings
- `POST /api/bookings/` - Create new booking
- `GET /api/bookings/{id}/` - Get specific booking
- `PUT /api/bookings/{id}/` - Update booking
- `DELETE /api/bookings/{id}/` - Cancel booking

### Reviews
- `GET /api/reviews/` - List reviews
- `POST /api/reviews/` - Create new review
- `GET /api/reviews/{id}/` - Get specific review
- `PUT /api/reviews/{id}/` - Update review
- `DELETE /api/reviews/{id}/` - Delete review

## Serializers

### ListingSerializer
- Handles listing data serialization
- Includes validation for dates and prices
- Calculates average rating

### BookingSerializer
- Handles booking data serialization
- Validates booking dates and guest capacity
- Automatically calculates total price

### ReviewSerializer
- Handles review data serialization
- Validates rating range (1-5)

## Model Features

### Constraints and Validations
- **Booking dates**: Check-out must be after check-in
- **Guest capacity**: Cannot exceed listing's max_guests
- **Price validation**: Must be positive values
- **Rating validation**: Must be between 1-5
- **Unique reviews**: One review per guest per listing

### Calculated Properties
- **average_rating**: Calculated from all reviews
- **duration_days**: Booking duration in days

## Development

### Run development server:
```bash
python manage.py runserver
```

### Run tests:
```bash
python manage.py test
```

### Access admin interface:
Visit `http://localhost:8000/admin/` and login with your superuser credentials.

## Sample Data

The seed command creates realistic sample data including:
- Users with varied names and profiles
- Listings in major US cities
- Bookings with different statuses
- Reviews with ratings biased toward positive experiences

## Project Structure

```
alx_travel_app/
├── listings/
│   ├── models.py          # Database models
│   ├── serializers.py     # API serializers
│   ├── management/
│   │   └── commands/
│   │       └── seed.py    # Database seeding command
│   └── ...
├── manage.py
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## License

This project is part of the ALX Software Engineering program.
