from os import stat
from django.urls import path, include
from distribution_tracker import views
from rumi_press import settings
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.home_page, name='home_page'),
    path('login/',views.user_login, name='user_login'),
    path('view_books/', views.view_books, name='view_books'),
    path('add_books/', views.add_books, name='add_books'),
   path('add_book_cat', views.add_book_cat, name='add_book_cat'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)