from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


app_name = 'main'

urlpatterns = [
    path('',views.landing,name='landing-page'),
    path('login/',auth_views.LoginView.as_view(template_name='main/login.html'),name='login-view'),
    path('logout/',auth_views.LogoutView.as_view(template_name='main/logout.html'),name='logout-view'),
    path('user/<str:username>',views.analytics_by_account,name='analytics-by-account'),
    path('topic/',views.analytics_by_topic,name='analytics-by-topic'),
    path('sentiment/<str:topic>',views.sentimentfilter,name='sentiment'),
    path('hashtag/',views.gethastag ,name='get-hashtags'),
    path('compare/',views.compete,name='user-comp'),
    path('register/',views.register,name='register-view')
]
