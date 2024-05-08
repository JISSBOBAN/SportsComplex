import pyrebase
from django.views import View

firebaseConfig = {
  "apiKey": "AIzaSyAY_uglVpg4vAHR2XA2Cn9v8aO_vBTG-9A",
  "authDomain": "sportscomplex-8c773.firebaseapp.com",
  "projectId": "sportscomplex-8c773",
  "databaseURL": "/",
  "storageBucket": "sportscomplex-8c773.appspot.com",
  "messagingSenderId": "586353141474",
  "appId": "1:586353141474:web:a8e1b59a9e43617d7b20bb",
  "measurementId": "G-MKPVQXTWHZ"
}

firebase = pyrebase.initialize_app(firebaseConfig)
database = firebase.database()
auth = firebase.auth()


class SignUp(View):
    def get(self, request):
        return render(request, 'signup.html')



    try:
        def post(self, request):
            name = request.POST['name']

            email = request.POST['email']
            password = request.POST['password']
            auth = firebase.auth()
            user = auth.create_user(name=name, email=email, password=password)
            #user = auth.create_user_with_email_and_password(email, password)
            #signin = auth.sign_in_with_email_and_password(email, password)
            auth.send_email_verification(user['idToken'])
            print("Email verification has been send")
            # auth.sign_in_with_email_and_password(email, password)
            #print("Signed in")
            return render(request, 'signin.html')

    except:
        print("Failed to Create User")


from django.shortcuts import render, redirect
from django.views import View
from firebase_admin import auth

class SignIn(View):
    def get(self, request):
        return render(request, 'signin.html')

    def post(self, request):
        try:
            email = request.POST['email']
            password = request.POST['password']

            # Authenticate user using Firebase
            user = auth.get_user_by_email(email)  # Retrieve user info by email
            #auth.verify_password(user, password)  # Verify user password

            # Redirect to 'bookings:book_view' with the user's email as a parameter
            return redirect('booking')

        except Exception as e:
            print(f"Error: {e}")
            # Handle invalid credentials (e.g., render error message on the signin page)
            return render(request, 'error.html', {'error_message': 'Invalid Credentials'})



class PR(View):

    def get(self, request):
        return render(request, 'signup.html')



    try:
        def post(self, request):
            email = request.POST['email']
            password = request.POST['password']
            auth = firebase.auth()
            auth.sign_in_with_email_and_password(email, password)
            auth.send_password_reset_email(email)
            print("We have send email reset, check your inbox")
            return render(request, 'pass.html')

    except:
        print("Failed to Create User")

