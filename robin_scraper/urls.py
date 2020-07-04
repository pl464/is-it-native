from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_not_used, name='pre_results'),
    path('about', views.get_about, name='about'),
    path('s/<search_term>', views.index_used, name='results'),
]