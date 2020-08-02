from django.urls import path
from .views import TwitterAPI, Analyzer, ReportAndBlock

urlpatterns = [
    path('twitter/', TwitterAPI.as_view()),
    path('analyze/', Analyzer.as_view()),
    path('block/', ReportAndBlock.as_view())
]
