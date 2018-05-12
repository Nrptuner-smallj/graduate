from django.urls import path


from .views import SearchView,DetailView,LackView,AddToShopCart,ToConfirmView,ConfirmInfoView,PayView

import users.views

app_name = 'commoditys'
urlpatterns = [
    path('list/',SearchView.as_view(),name='list'),
    path('detail/<str:commodity_id>/',DetailView.as_view(),name="detail"),
    path('lack/',LackView.as_view(),name="lack"),
    path('addtocart/',AddToShopCart.as_view(),name='addtocart'),
    path('toconfirm/',ToConfirmView.as_view(),name='toconfirm'),
    path('confirminfo/',ConfirmInfoView.as_view(),name='confirminfo'),
    path('pay/',PayView.as_view(),name='pay'),

]