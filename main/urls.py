from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.landing,name='landing-page'),
    path('<str:username>',views.analytics_by_account,name='analytics-by-account')
]
