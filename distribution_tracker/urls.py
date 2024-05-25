from django.urls import path, include
from distribution_tracker import views


urlpatterns = [
    path('',views.home_page, name='home_page'),
]