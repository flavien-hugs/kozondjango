"""core URL Configuration
"""

from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView,
    PasswordChangeView, PasswordChangeDoneView)

from dashboard.views import DashboardListView

urlpatterns = [
    path('', DashboardListView.as_view(), name='home'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('reset/', PasswordResetView.as_view(
        template_name='accounts/password_reset.html',
        email_template_name='accounts/password_reset_email.html',
        subject_template_name='accounts/password_reset_subject.txt'
    ), name='password_reset'),
    path('reset/done/', PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'),
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('reset/complete/', PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'),
        name='password_reset_complete'),
    path('password/change/', PasswordChangeView.as_view(
        template_name='accounts/password_change.html'),
        name='password_change'),
    path('password/done/', PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'),
        name='password_change_done'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
