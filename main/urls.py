from django.urls import path, include
from . import views

app_name = 'main'

urlpatterns = [
    path('',views.landing,name='landing-page'),
    path('user/<str:username>',views.analytics_by_account,name='analytics-by-account'),
    path('topic/<str:topic>',views.analytics_by_topic,name='analytics-by-topic'),
    path('user/<str:username>/<str:mode>',views.likes_per_post,name='likes-per-post')
]
