from django.urls import path

from .views import RegisterView, GetEmailCodeView, LoginView, LogoutView, ForgetPwdView, UserCenterIndexView,ModifyPwdView
from .views import ModifyEmailView,AddressListView,AddAddressView


app_name = 'users'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('sendemail', GetEmailCodeView.as_view(), name="getcode"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('forgetpwd/', ForgetPwdView.as_view(), name="forgetpwd"),
    path('usercenterinfo/', UserCenterIndexView.as_view(), name="usercenter"),
    path('modifypwd/',ModifyPwdView.as_view(),name="modifypwd"),
    path('modifyemail/',ModifyEmailView.as_view(),name="modifyeamil"),
    path('addresslist/',AddressListView.as_view(),name="addresslist"),
    path('addaddress/<int:address_id>',AddAddressView.as_view(),name="addaddress"),
]
