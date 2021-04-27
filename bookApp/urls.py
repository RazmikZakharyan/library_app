from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('accounts/', include('UserApp.urls'), name='login'),
    path('pdf/<slug:book_slug>/', views.PDFView.as_view(), name='pdf'),
    path('genre/<slug:genre_slug>/', views.BookListView.as_view(), name='genre'),
    path('title/<slug:book_slug>/', views.BookDetailView.as_view(), name='book_single'),
    path('author/<slug:author_slug>/', views.AuthorDetailView.as_view(), name='author'),

]
