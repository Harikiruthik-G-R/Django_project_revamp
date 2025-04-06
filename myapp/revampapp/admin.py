# from mongoengine.django.mongo_admin import DocumentAdmin
# from django_mongoengine.mongo_admin import site
# from .models import Users, Product

# class UsersAdmin(DocumentAdmin):
#     list_display = ('full_name', 'email', 'phone_number', 'is_active', 'date_joined', 'last_login')
#     search_fields = ('full_name', 'email', 'phone_number')
#     list_filter = ('is_active',)
#     readonly_fields = ('date_joined', 'last_login')

# class ProductAdmin(DocumentAdmin):
#     list_display = ('title', 'brand', 'model', 'price', 'condition', 'location', 'created_at')
#     search_fields = ('title', 'brand', 'model', 'location')
#     list_filter = ('condition', 'fuel_type', 'transmission', 'color')

# # Registering documents
# site.register(Users, UsersAdmin)
# site.register(Product, ProductAdmin)
