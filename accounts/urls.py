from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('login/', views.SignIn.as_view(), name='login'),  # Corrected to use views.SignIn.as_view()
    path('pr/', views.PR.as_view(), name='PR'),
]
