
# models.py
from django.contrib.auth.models import AbstractUser, Group,Permission
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)

    # Define unique related_name attributes to avoid conflicts
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Unique name for reverse relationship
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',  # Unique name for reverse relationship
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='custom_user',
    )

class Train(models.Model):
    train_id = models.CharField(max_length=10, unique=True)
    train_name = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    total_seats = models.IntegerField()
    available_seats = models.IntegerField(default=10)  # You can remove this if you calculate dynamically

    def update_available_seats(self):
        # Update available seats dynamically based on bookings
        booked_seats = Booking.objects.filter(train=self).count()
        self.available_seats = self.total_seats - booked_seats
        self.save()

    def __str__(self):
        return self.train_name

class Seat(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"Seat {self.seat_number} ({'Booked' if self.is_booked else 'Available'})"

# models.py
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now) 

    def __str__(self):
        return f"Booking for {self.user.username} on {self.train.train_name} - Seat {self.seat.seat_number}"