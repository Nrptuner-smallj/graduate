from django.urls import path

from .views import RegisterView,GetEmailCodeView,LoginView,LogoutView
import users.views

app_name = 'users'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('sendemail',GetEmailCodeView.as_view(),name = "getcode"),
    path('login/',LoginView.as_view(),name = "login"),
    path('logout/',LogoutView.as_view(),name ="logout"),
]
