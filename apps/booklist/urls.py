from django.urls import path

from .views import EditBookListView,MyBookListView,DelBookListView,AddBookView,SearchBookListView

app_name = 'booklist'
urlpatterns = [
    path('mybooklist/',MyBookListView.as_view(),name='mybooklist'),
    path('delbooklist/<int:booklist_id>/',DelBookListView.as_view(),name='delbooklist'),
    path('editbooklist/<int:booklist_id>/', EditBookListView.as_view(), name='editbooklist'),
    path('addbook/',AddBookView.as_view(),name='addbook'),
    path('search/',SearchBookListView.as_view(),name='search'),

]
