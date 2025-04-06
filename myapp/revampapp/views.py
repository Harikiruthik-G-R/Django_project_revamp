from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Users, Product
import os
from django.conf import settings
import uuid

def signup(request):
    if request.method == 'POST':
        full_name = request.POST.get('fullname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        
        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, 'signup.html')
        
        # Check if user already exists
        if Users.get_by_email(email):
            messages.error(request, "Email already registered")
            return render(request, 'signup.html')
        
        try:
            # Create new user using the create_user method from your model
            Users.create_user(full_name, email, phone, password)
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')
        except ValueError as e:
            messages.error(request, str(e))
            return render(request, 'signup.html')
    
    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = Users.get_by_email(email)
        
        if user and user.check_password(password):
            # Update last login time
            user.update_last_login()
            
            # In a real app, you'd set up a session here
            # For example with Django's session framework:
            request.session['user_id'] = str(user.id)
            request.session['user_email'] = user.email
            request.session['user_name'] = user.full_name
            
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password")
            return render(request, 'login.html')
    
    return render(request, 'login.html')

def sell(request):
    # Check if user is logged in
    user_id = request.session.get('user_id')
    
    if not user_id:
        # Redirect to login if not authenticated
        messages.error(request, "Please log in to sell products")
        return redirect('login')
    
    if request.method == 'POST':
        # Get form data
        product_type = request.POST.get('product_type')
        title = request.POST.get('title')
        brand = request.POST.get('brand')
        model = request.POST.get('model')
        year = request.POST.get('year', '')
        condition = request.POST.get('condition')
        price = request.POST.get('price')
        mileage = request.POST.get('mileage', '')
        fuel_type = request.POST.get('fuel_type', '')
        transmission = request.POST.get('transmission', '')
        color = request.POST.get('color', '')
        location = request.POST.get('location')
        description = request.POST.get('description')
        seller_phone = request.POST.get('seller_phone')
        seller_identification = request.POST.get('seller_identification')
        
        # Handle image upload
        if 'product_image' in request.FILES:
            image_file = request.FILES['product_image']
            # Generate unique filename
            file_extension = os.path.splitext(image_file.name)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            
            # Save file to media directory
            upload_path = os.path.join(settings.MEDIA_ROOT, unique_filename)
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)
            
            print(f"Saving image to: {upload_path}")
            
            with open(upload_path, 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
            
            # Also save to static folder for direct access
            static_path = os.path.join(settings.BASE_DIR, 'revampapp', 'static', 'uploads', unique_filename)
            os.makedirs(os.path.dirname(static_path), exist_ok=True)
            
            print(f"Also saving image to static folder: {static_path}")
            
            with open(static_path, 'wb+') as destination:
                image_file.seek(0)  # Reset file pointer
                for chunk in image_file.chunks():
                    destination.write(chunk)
            
            # Store relative path in database - just the filename
            image_path = unique_filename
            print(f"Image path stored in database: {image_path}")
        else:
            image_path = ""
        
        try:
            # Create product in database
            product = {
                'product_type': product_type,
                'title': title,
                'brand': brand,
                'model': model,
                'year': year,
                'condition': condition,
                'price': int(price),
                'mileage': mileage,
                'fuel_type': fuel_type,
                'transmission': transmission,
                'color': color,
                'location': location,
                'description': description,
                'seller_id': user_id,
                'seller_phone': seller_phone,
                'seller_identification': seller_identification,
                'image': image_path
            }
            
            Product.create_product(product)
            messages.success(request, "Your product has been listed successfully!")
            return redirect('home')
        except Exception as e:
            messages.error(request, f"Error creating listing: {str(e)}")
            return render(request, 'sell.html', {'is_authenticated': True, 'user_name': request.session.get('user_name')})
    
    return render(request, 'sell.html', {'is_authenticated': True, 'user_name': request.session.get('user_name')})

def home(request):
    # Check if user is logged in
    user_id = request.session.get('user_id')
    
    context = {}
    if user_id:
        # User is logged in
        context['user_name'] = request.session.get('user_name')
        context['is_authenticated'] = True
    else:
        context['is_authenticated'] = False
    
    # Get featured products from database
    try:
        products = Product.get_featured_products(limit=8)
        context['products'] = products
    except Exception as e:
        # If there's an error, we'll just show the page without products
        print(f"Error fetching products: {str(e)}")
    
    return render(request, 'index.html', context)

# Add this new function to handle static product details
def static_product_detail(request, product_id):
    # Get the static product data based on the ID
    static_products = {
        1: {
            'title': 'Honda Civic 2022',
            'price': '₹8,00,500',
            'mileage': '15,000 miles',
            'location': 'San Francisco, CA',
            'condition': 'used',
            'product_type': 'car',
            'brand': 'honda',
            'image': 'images/honda-civic.webp',
            'description': 'This Honda Civic 2022 is in excellent condition and has been well-maintained. It comes with all standard features and has passed all necessary inspections.',
            # Add these fields to match the template expectations
            'make': 'Honda',
            'model': 'Civic',
            'year': '2022',
            'fuel_type': 'Petrol',
            'transmission': 'Automatic',
            'color': 'Red',
            'seller_name': 'John Doe',
            'seller_since': 'January 2020'
        },
        2: {
            'title': 'Yamaha YZF-R1 2021',
            'price': '₹2,00,750',
            'mileage': '8,500 miles',
            'location': 'Portland, OR',
            'condition': 'new',
            'product_type': 'bike',
            'brand': 'yamaha',
            'image': 'images/yamaha.webp',
            'description': 'This Yamaha YZF-R1 2021 is in excellent condition and has been well-maintained. It comes with all standard features and has passed all necessary inspections.',
            # Add these fields to match the template expectations
            'make': 'Yamaha',
            'model': 'YZF-R1',
            'year': '2021',
            'fuel_type': 'Petrol',
            'transmission': 'Manual',
            'color': 'Blue',
            'seller_name': 'Jane Smith',
            'seller_since': 'March 2019'
        },
        3: {
            'title': 'BMW X5 2020',
            'price': '₹7,00,900',
            'mileage': '25,000 miles',
            'location': 'Chicago, IL',
            'condition': 'used',
            'product_type': 'car',
            'brand': 'bmw',
            'image': 'images/BMW.webp',
            'description': 'This BMW X5 2020 is in excellent condition and has been well-maintained. It comes with all standard features and has passed all necessary inspections.',
            # Add these fields to match the template expectations
            'make': 'BMW',
            'model': 'X5',
            'year': '2020',
            'fuel_type': 'Diesel',
            'transmission': 'Automatic',
            'color': 'Black',
            'seller_name': 'Robert Johnson',
            'seller_since': 'June 2018'
        },
        4: {
            'title': 'Harley-Davidson Street Glide',
            'price': '₹9,19,800',
            'mileage': '12,400 miles',
            'location': 'Austin, TX',
            'condition': 'used',
            'product_type': 'bike',
            'brand': 'harley davidson',
            'image': 'images/Harley.webp',
            'description': 'This Harley-Davidson Street Glide is in excellent condition and has been well-maintained. It comes with all standard features and has passed all necessary inspections.',
            # Add these fields to match the template expectations
            'make': 'Harley-Davidson',
            'model': 'Street Glide',
            'year': '2019',
            'fuel_type': 'Petrol',
            'transmission': 'Manual',
            'color': 'Black',
            'seller_name': 'Michael Brown',
            'seller_since': 'November 2017'
        }
    }
    
    product = static_products.get(product_id)
    
    if not product:
        # Handle case where product is not found
        return redirect('home')
    
    context = {
        'product': product,
        'is_authenticated': request.session.get('user_id') is not None,
        'user_name': request.session.get('user_name', ''),
    }
    
    return render(request, 'product_detail.html', context)

def logout(request):
    # Clear session
    request.session.flush()
    return redirect('home')

def uploaded_product_detail(request, product_id):
    # Check if user is logged in
    user_id = request.session.get('user_id')
    
    print(f"Accessing product_detail with product_id: {product_id}")
    
    context = {}
    if user_id:
        # User is logged in
        context['user_name'] = request.session.get('user_name')
        context['is_authenticated'] = True
    else:
        context['is_authenticated'] = False
    
    # Get product from database
    try:
        print(f"Attempting to retrieve product with ID: {product_id}")
        product = Product.get_by_id(product_id)
        print(f"Retrieved product: {product}")
        
        if not product:
            print("Product not found, redirecting to home")
            messages.error(request, "Product not found")
            return redirect('home')
        
        # Debug the image path
        if hasattr(product, 'image') and product.image:
            print(f"Image filename in database: {product.image}")
            
            # Check if the file exists
            image_path = os.path.join(settings.MEDIA_ROOT, product.image)
            print(f"Full image path on server: {image_path}")
            print(f"File exists: {os.path.exists(image_path)}")
            
            # Also check the static uploads folder
            static_path = os.path.join(settings.BASE_DIR, 'revampapp', 'static', 'uploads', product.image)
            print(f"Static path: {static_path}")
            print(f"File exists in static: {os.path.exists(static_path)}")
        
        context['product'] = product
    except Exception as e:
        print(f"Error retrieving product: {str(e)}")
        messages.error(request, f"Error retrieving product: {str(e)}")
        return redirect('home')
    
    return render(request, 'uploaded_product_detail.html', context)

def car(request):
    # Check if user is logged in
    user_id = request.session.get('user_id')
    
    context = {}
    if user_id:
        # User is logged in
        context['user_name'] = request.session.get('user_name')
        context['is_authenticated'] = True
    else:
        context['is_authenticated'] = False
    
    # Get car products from database (filter by product_type='car')
    try:
        # Modify this to get only car products
        car_products = Product.objects.filter(product_type='car')
        context['car_products'] = car_products
    except Exception as e:
        # If there's an error, we'll just show the page without products
        print(f"Error fetching car products: {str(e)}")
    
    return render(request, 'cars.html', context)

def contact(request):
    return render(request, 'contact.html')

def bike(request):
    # Check if user is logged in
    user_id = request.session.get('user_id')
    
    context = {}
    if user_id:
        # User is logged in
        context['user_name'] = request.session.get('user_name')
        context['is_authenticated'] = True
    else:
        context['is_authenticated'] = False
    
    # Get bike products from database (filter by product_type='bike')
    try:
        # Get only bike products
        bike_products = Product.objects.filter(product_type='bike')
        context['bike_products'] = bike_products
        print(f"Successfully fetched {len(bike_products)} bike products")
    except Exception as e:
        # If there's an error, we'll just show the page without products
        print(f"Error fetching bike products: {str(e)}")
        messages.error(request, "Unable to load bike listings at this time")
    
    return render(request, 'bikes.html', context)


def parts(request):
    # Check if user is logged in
    user_id = request.session.get('user_id')
    
    context = {}
    if user_id:
        # User is logged in
        context['user_name'] = request.session.get('user_name')
        context['is_authenticated'] = True
    else:
        context['is_authenticated'] = False
    
    # Get parts products from database (filter by product_type='parts')
    try:
        # Get only parts products
        parts_products = Product.objects.filter(product_type='parts')
        context['parts_products'] = parts_products
        print(f"Successfully fetched {len(parts_products)} parts products")
    except Exception as e:
        # If there's an error, we'll just show the page without products
        print(f"Error fetching parts products: {str(e)}")
        messages.error(request, "Unable to load parts listings at this time")
    
    return render(request, 'parts.html', context)