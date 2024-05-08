import firebase_admin
from django.views import View
from firebase_admin import credentials
import os
from django.shortcuts import render
from firebase_admin import firestore
from google.cloud.exceptions import NotFound
from django.shortcuts import redirect
from firebase_admin import db


key_file_path = os.path.join(os.path.dirname(__file__), '..', 'key.json')
cred = credentials.Certificate(key_file_path)
firebase_admin.initialize_app(cred)

db = firestore.client()

def home(request):
    return render(request, 'home.html')
# Now you can use Firebase services such as Firestore, Realtime Database, etc.


# class BookingView(View):
#     def get(self, request, email):
#         return render(request, 'book.html')
#
#     def post(self, request, email):
#         try:
#             sports = request.POST['sports']
#             date = request.POST['date']
#             time = request.POST['time']
#             # Create booking data dictionary
#
#             # Store booking data in Firebase
#             doc_ref = db.collection('bookings').document()
#             doc_ref.set({
#                 'email': email,
#                 'sports': sports,
#                 'date': date,
#                 'time': time,
#
#             })
#             print("Booking created successfully!")
#             return render(request, 'home.html')  # Render success page after booking
#         except Exception as e:
#             return render(request, 'book.html')

class SignInStaff(View):
    def get(self, request):
        return render(request, 'signin.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the provided email matches the staff email
        if email == "gouribiju195@gmail.com":
           return redirect('/staff')
def staff_booking_view(request):
    # Initialize Firestore client

    # Perform Firestore query for cricket bookings
    query = db.collection('bookings').where('sport_type', '==', 'cricket').get()

    # Prepare query results to be passed to template
    cricket_bookings = []
    for doc in query:
        cricket_bookings.append(doc.to_dict())

    context = {
        'cricket_bookings': cricket_bookings
    }

    return render(request, 'staff_booking_view.html', context)


def booking(request):
    return render(request, 'booking.html')


# views.py


def confirm_date(request):
    if request.method == 'POST':
        selected_date = request.POST.get('selected_date')
        sport_type = request.POST.get('sport_type')  # Use 'sport_type' instead of 'sports'
        return redirect('timeslot', selected_date=selected_date, sport_type=sport_type)  # Use 'sport_type' here
    return redirect('booking')


def timeslot(request, selected_date, sport_type):
    try:
        # Get Firestore client

        # Query Firestore for bookings on the selected date and for the specified sport
        bookings_ref = db.collection('bookings').where('selected_date', '==', selected_date).where('sport_type', '==', sport_type)

        # Fetch booked slots from Firestore
        booked_slots = [bookings.to_dict() for bookings in bookings_ref.stream()]

        # Extract booked times from fetched bookings
        booked_times = [bookings['selected_slot'] for bookings in booked_slots]

        # Define all available time slots (customize based on your requirements)
        all_slots = [
            '6:00 AM - 7:00 AM',
            '7:00 AM - 8:00 AM',
            '8:00 AM - 9:00 AM',
            '9:00 AM - 10:00 AM',
            '10:00 AM - 11:00 AM',
            '11:00 AM - 12:00 PM',
            '12:00 PM - 1:00 PM',
            # Add more time slots as needed
        ]

        # Filter available time slots to exclude booked slots
        available_slots = [slot for slot in all_slots if slot not in booked_times]

        # Render timeslot.html template with selected_date, sports, and available_slots
        return render(request, 'timeslot.html',
                      {'selected_date': selected_date, 'sport_type': sport_type, 'available_slots': available_slots})

    except NotFound as e:
        # Handle Firestore collection not found error
        error_message = f"Firestore collection 'bookings' not found: {str(e)}"
        return render(request, 'error.html', {'error_message': error_message})

    except Exception as e:
        # Handle other exceptions (e.g., Firestore query errors)
        error_message = f"An error occurred: {str(e)}"
        return render(request, 'error.html', {'error_message': error_message})


def confirm_timeslot(request):
    if request.method == 'POST':
        selected_date = request.POST.get('selected_date')
        sport_type = request.POST.get('sport_type')
        selected_slot = request.POST.get('selected_slot')
        # Assuming sport_type is passed
        user_email = request.user.email
        bookings_ref = db.collection('bookings')

        # Add a new document to the 'bookings' collection
        bookings_ref.add({
            'user_email': user_email,
            'selected_date': selected_date,
            'sport_type': sport_type,
            'selected_slot': selected_slot
        })

        return redirect('success')
    return redirect('booking')


def success(request):
    return render(request, 'success.html')

# views.py

from django.shortcuts import render
from firebase_admin import firestore
from django.contrib.auth.decorators import login_required

# views.py

from django.shortcuts import render
from firebase_admin import firestore
from django.contrib.auth.decorators import login_required

@login_required
def user_bookings(request):
    current_user_email = request.user.email
    db = firestore.client()

    bookings_ref = db.collection('bookings')
    query = bookings_ref.where('user_email', '==', current_user_email).get()

    bookings = []
    for booking in query:
        # Define booking_data dictionary for each booking
        booking_data = {
            'id': booking.id,
            'selected_date': booking.get('selected_date'),
            'selected_slot': booking.get('selected_slot'),
            'sport_type': booking.get('sport_type'),
            'user_email': booking.get('user_email')
        }
        # Add cancellation URL to each booking data
        cancellation_url = f"/cancel-booking/{booking.id}/"
        booking_data['cancellation_url'] = cancellation_url

        # Append booking_data to bookings list
        bookings.append(booking_data)

    return render(request, 'bookings.html', {'bookings': bookings})

# views.py

from django.shortcuts import redirect
from firebase_admin import firestore
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound

@login_required
def cancel_booking(request, booking_id):
    db = firestore.client()
    booking_ref = db.collection('bookings').document(booking_id)

    # Check if the booking exists
    booking_doc = booking_ref.get()
    if not booking_doc.exists:
        return HttpResponseNotFound("Booking not found")


    # Delete the booking document from Firestore
    booking_ref.delete()

    # Redirect back to the user bookings page after cancellation
    return redirect('user_bookings')
