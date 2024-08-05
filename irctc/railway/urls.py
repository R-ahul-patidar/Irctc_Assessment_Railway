# railway/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, TrainViewSet, SeatViewSet, BookingViewSet
from . import views

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'trains', TrainViewSet)
router.register(r'seats', SeatViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'), 
    path('make_booking/', views.make_booking, name='make_booking'),
    # path('book/<int:train_id>/', views.book_ticket, name='book_ticket'),
]
