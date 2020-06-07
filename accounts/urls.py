from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from accounts.views import signup, UserUpdateView

app_name = 'accounts'
urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', LoginView.as_view(
        template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('ac/', UserUpdateView.as_view(), name='account'),
]
