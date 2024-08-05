from django.shortcuts import render,redirect,get_object_or_404

# Create your views here.
# views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.contrib.auth import authenticate, login as auth_login,login
from .models import User, Train, Seat, Booking
from .serializers import UserSerializer, TrainSerializer, SeatSerializer, BookingSerializer
from rest_framework.authtoken.models import Token
from django.db import transaction
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import BookingForm 
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .forms import BookingForm

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer
    permission_classes = [IsAdminUser]

class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    permission_classes = [IsAdminUser]

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def book_seat(self, request):
        train_id = request.data.get('train_id')
        with transaction.atomic():
            train = Train.objects.select_for_update().get(train_id=train_id)
            available_seat = Seat.objects.filter(train=train, is_available=True).first()
            if available_seat:
                available_seat.is_available = False
                available_seat.save()
                booking = Booking.objects.create(user=request.user, train=train, seat=available_seat)
                return Response({'booking_id': booking.id}, status=status.HTTP_201_CREATED)
        return Response({'error': 'No available seats'}, status=status.HTTP_400_BAD_REQUEST)


class CustomUserCreationForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    password_confirm = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match")

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already taken'})
        user = User(username=username, email=email, password=make_password(password1))
        user.save()
        return redirect('login')
    return render(request, 'signup.html')


def home(request):
    return render(request, 'home.html')



# New view for user dashboard

def user_dashboard(request):
    user = request.user
    bookings = Booking.objects.filter(user=user)  # Fetch all bookings for the user
    trains = Train.objects.all()  # Fetch all available trains
    forms = BookingForm()  # Create an instance of the booking form
   
    context={
        
        'user': user,
        'bookings': bookings,
        'trains': trains,
        'form': forms
    }
    
    return render(request, 'user_dashboard.html', context)


# View to handle new bookings
def make_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            train_id = request.POST.get('train_id')
            train = Train.objects.get(id=train_id)
            available_seat = Seat.objects.filter(is_booked=False).first()

            if available_seat:
                booking = form.save(commit=False)
                booking.user = request.user
                booking.seat = available_seat
                booking.save()
                
                # Mark the seat as booked
                available_seat.is_booked = True
                available_seat.save()
                
                # Update available seats in train
                train.update_available_seats()
                
                messages.success(request, f"Booking successful! Your seat number is {available_seat.seat_number}. Thank you!")
                return redirect('user_dashboard')
            else:
                messages.error(request, "No seats available at the moment.")
                return redirect('user_dashboard')
    return redirect('user_dashboard')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('user_dashboard')  # or another page
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')



def book_ticket(request, train_id):
    train = get_object_or_404(Train, id=train_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid() and train.available_seats > 0:
            # Process the booking (e.g., create a booking record)
            train.available_seats -= 1
            train.save()
            # Redirect or show success message
            return redirect('success_page')  # Change to your success page
    else:
        form = BookingForm()
    return render(request, 'book_ticket.html', {'form': form, 'train': train})