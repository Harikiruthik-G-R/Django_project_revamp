from mongoengine import Document, StringField, EmailField, DateTimeField, BooleanField, IntField, ReferenceField, FloatField
from django.contrib.auth.hashers import make_password, check_password
import datetime
import re

class Users(Document):
    full_name = StringField(required=True, max_length=100)
    email = EmailField(required=True, unique=True)
    phone_number = StringField(required=True, max_length=20)
    password_hash = StringField(required=True)
    is_active = BooleanField(default=True)
    date_joined = DateTimeField(default=datetime.datetime.now)
    last_login = DateTimeField()
    
    meta = {
        'collection': 'users',
        'indexes': [
            {'fields': ['email'], 'unique': True}
        ]
    }
    
    @staticmethod
    def validate_password(password):
        """
        Validates password strength.
        Returns an error message if invalid, or None if valid.
        """
        if len(password) < 8:
            return "Password must be at least 8 characters long."
        if not re.search(r'[A-Z]', password):
            return "Password must contain at least one uppercase letter."
        if not re.search(r'[a-z]', password):
            return "Password must contain at least one lowercase letter."
        if not re.search(r'\d', password):
            return "Password must contain at least one digit."
        if not re.search(r'[@$!%*?&]', password):
            return "Password must contain at least one special character (@$!%*?&)."
        
        return None  # Password is valid
    
    @staticmethod
    def validate_phone(phone):
        """
        Validates phone number format
        Returns True if valid, False otherwise
        """
        # Basic phone validation - can be customized based on your requirements
        pattern = r'^\+?[0-9]{10,15}$'  # Between 10-15 digits with optional + prefix
        return bool(re.match(pattern, phone))
    
    def set_password(self, raw_password):
        """
        Sets the user's password - converts to a Django compatible hash
        """
        self.password_hash = make_password(raw_password)
        
    def check_password(self, raw_password):
        """
        Checks if the provided password matches the stored hash
        """
        return check_password(raw_password, self.password_hash)
    
    def update_last_login(self):
        """
        Updates the last login timestamp
        """
        self.last_login = datetime.datetime.now()
        self.save()
    
    @classmethod
    def create_user(cls, full_name, email, phone_number, password):
        """
        Creates and saves a new user with given details
        """
        if not cls.validate_password(password):
            raise ValueError("Password does not meet security requirements")
        
        if not cls.validate_phone(phone_number):
            raise ValueError("Invalid phone number format")
        
        user = cls(
            full_name=full_name,
            email=email.lower(),  # Store emails in lowercase for consistency
            phone_number=phone_number
        )
        user.set_password(password)
        user.save()
        return user
    
    @classmethod
    def get_by_email(cls, email):
        """
        Returns a user by email
        """
        try:
            return cls.objects.get(email=email.lower())
        except cls.DoesNotExist:
            return None
    
    def __str__(self):
        return f"{self.full_name} ({self.email})"


class Product(Document):
    product_type = StringField(required=True)
    title = StringField(required=True)
    brand = StringField(required=True)
    model = StringField(required=True)
    year = StringField()
    condition = StringField(required=True)
    price = IntField(required=True)
    mileage = StringField()
    fuel_type = StringField()
    transmission = StringField()
    color = StringField()
    location = StringField(required=True)
    description = StringField(required=True)
    seller_id = StringField(required=True)
    seller_phone = StringField(required=True)
    seller_identification = StringField(required=True)
    image = StringField()
    created_at = DateTimeField(default=datetime.datetime.now)
    
    @classmethod
    def create_product(cls, product_data):
        """
        Create a new product listing in the database
        """
        product = cls(**product_data)
        product.save()
        return product
    
    @classmethod
    def get_featured_products(cls, limit=8):
        """
        Get featured products for the homepage
        """
        return cls.objects.order_by('-created_at').limit(limit)
    
    @classmethod
    def get_by_id(cls, product_id):
        """Returns a product by its ID"""
        try:
            return cls.objects.get(id=product_id)
        except cls.DoesNotExist:
            return None