from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User as AuthUser
from .models import User, Train, Seat, Booking

# Define a custom User admin
class UserAdmin(BaseUserAdmin):
    model = User

    # The fields to be used in displaying the User model.
    # These override the default fields from BaseUserAdmin
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    # Fields to be used when adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name'),
        }),
    )
    # Display the following fields in the list view of the User model
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    # Add search functionality for these fields
    search_fields = ('username', 'email', 'first_name', 'last_name')
    # Order users by username
    ordering = ('username',)

# Register the User model with the custom UserAdmin
admin.site.register(User, UserAdmin)

# Register other models
admin.site.register(Train)
admin.site.register(Seat)
admin.site.register(Booking)
