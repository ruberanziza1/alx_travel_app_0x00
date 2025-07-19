from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Listing, Booking, Review

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        read_only_fields = ['id']

class ListingSerializer(serializers.ModelSerializer):
    """Serializer for Listing model"""
    host = UserSerializer(read_only=True)
    average_rating = serializers.ReadOnlyField()
    
    class Meta:
        model = Listing
        fields = [
            'listing_id', 'host', 'title', 'description', 'location',
            'price_per_night', 'bedrooms', 'bathrooms', 'max_guests',
            'available_from', 'available_to', 'created_at', 'updated_at',
            'average_rating'
        ]
        read_only_fields = ['listing_id', 'created_at', 'updated_at', 'average_rating']
    
    def validate(self, data):
        """Custom validation for listing"""
        if data.get('available_to') and data.get('available_from'):
            if data['available_to'] <= data['available_from']:
                raise serializers.ValidationError(
                    "Available to date must be after available from date."
                )
        return data
    
    def validate_price_per_night(self, value):
        """Validate price per night"""
        if value <= 0:
            raise serializers.ValidationError("Price per night must be greater than 0.")
        return value

class BookingSerializer(serializers.ModelSerializer):
    """Serializer for Booking model"""
    listing = ListingSerializer(read_only=True)
    guest = UserSerializer(read_only=True)
    listing_id = serializers.UUIDField(write_only=True)
    duration_days = serializers.ReadOnlyField()
    
    class Meta:
        model = Booking
        fields = [
            'booking_id', 'listing', 'guest', 'listing_id',
            'check_in_date', 'check_out_date', 'number_of_guests',
            'total_price', 'status', 'created_at', 'updated_at',
            'duration_days'
        ]
        read_only_fields = ['booking_id', 'created_at', 'updated_at', 'duration_days']
    
    def validate(self, data):
        """Custom validation for booking"""
        # Check dates
        if data['check_out_date'] <= data['check_in_date']:
            raise serializers.ValidationError(
                "Check-out date must be after check-in date."
            )
        
        # Check guest capacity
        listing = Listing.objects.get(listing_id=data['listing_id'])
        if data['number_of_guests'] > listing.max_guests:
            raise serializers.ValidationError(
                f"Number of guests ({data['number_of_guests']}) exceeds maximum allowed ({listing.max_guests})."
            )
        
        # Check availability dates
        if (data['check_in_date'] < listing.available_from or 
            data['check_out_date'] > listing.available_to):
            raise serializers.ValidationError(
                f"Booking dates must be within availability period ({listing.available_from} to {listing.available_to})."
            )
        
        return data
    
    def create(self, validated_data):
        """Create booking with calculated total price"""
        listing_id = validated_data.pop('listing_id')
        listing = Listing.objects.get(listing_id=listing_id)
        
        # Calculate total price
        duration = (validated_data['check_out_date'] - validated_data['check_in_date']).days
        total_price = listing.price_per_night * duration
        
        booking = Booking.objects.create(
            listing=listing,
            total_price=total_price,
            **validated_data
        )
        return booking

class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model"""
    guest = UserSerializer(read_only=True)
    listing = ListingSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'review_id', 'listing', 'guest', 'rating',
            'comment', 'created_at', 'updated_at'
        ]
        read_only_fields = ['review_id', 'created_at', 'updated_at']
    
    def validate_rating(self, value):
        """Validate rating is between 1 and 5"""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

# Additional serializers for different use cases
class ListingCreateSerializer(serializers.ModelSerializer):
    """Simplified serializer for creating listings"""
    class Meta:
        model = Listing
        fields = [
            'title', 'description', 'location', 'price_per_night',
            'bedrooms', 'bathrooms', 'max_guests',
            'available_from', 'available_to'
        ]
    
    def validate(self, data):
        """Custom validation for listing creation"""
        if data['available_to'] <= data['available_from']:
            raise serializers.ValidationError(
                "Available to date must be after available from date."
            )
        return data

class BookingCreateSerializer(serializers.ModelSerializer):
    """Simplified serializer for creating bookings"""
    class Meta:
        model = Booking
        fields = [
            'listing_id', 'check_in_date', 'check_out_date', 'number_of_guests'
        ]
    
    def validate(self, data):
        """Custom validation for booking creation"""
        if data['check_out_date'] <= data['check_in_date']:
            raise serializers.ValidationError(
                "Check-out date must be after check-in date."
            )
        return data
