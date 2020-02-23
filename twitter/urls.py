from django.urls import path
from .views import TwitterAPI, Analyzer

urlpatterns = [
    path('twitter/', TwitterAPI.as_view()),
    path('analyze/', Analyzer.as_view())
]