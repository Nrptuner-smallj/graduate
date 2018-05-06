from django.urls import path


from .views import SearchView,DetailView

import users.views

app_name = 'commoditys'
urlpatterns = [
    path('list/',SearchView.as_view(),name='list'),
    path('detail/<str:commodity_id>/',DetailView.as_view(),name="detail"),
]