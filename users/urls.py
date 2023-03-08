from django.urls import path

from users.views import LogInView, SignUpView, sign_out, ProfileView


urlpatterns = [
    path('login', LogInView.as_view(), name="login"),
    path('signup', SignUpView.as_view(), name="signup"),
    path('signout', sign_out, name='signout'),
    path('profile/<pk>', ProfileView.as_view(), name='profile'),
]
