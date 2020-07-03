from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.index_not_used, name='pre_results'),
    path('<search_term>', views.index_used, name='results'),
    path('about/', TemplateView.About.as_view(template_name="about.html")),
]