# urls.py

from django.urls import path
from . import views
from .views import user_bookings, cancel_booking
urlpatterns = [
    # Assuming 'sport_type' as the parameter name in the URL pattern
    path('', views.home, name='home'),
    path('cancel-booking/<str:booking_id>/', cancel_booking, name='cancel_booking'),
    path('user/bookings/', user_bookings, name='user_bookings'),
    path('signinstaff/', views.SignInStaff.as_view(), name='SignInStaff'),
    path('staff/', views.staff_booking_view, name='staff_booking_view'),
    path('timeslot/<str:selected_date>/<str:sport_type>/', views.timeslot, name='timeslot'),
    path('booking/', views.booking, name='booking'),
    path('booking/confirm_date/', views.confirm_date, name='confirm_date'),
    path('booking/confirm_timeslot/', views.confirm_timeslot, name='confirm_timeslot'),
    path('success/', views.success, name='success'),
]
