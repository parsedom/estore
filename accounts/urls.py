from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('profile', views.ProfileView.as_view(), name='profile'),

    path('activate/<uidb64>/<token>', views.activate_profile, name='registration_activation'),

]
