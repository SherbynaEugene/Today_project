from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

app_name = 'profile_app'

urlpatterns = [
    path('', views.profile_view, name='main'),
    path('buy/<slug:item_slug>/', views.buy_item, name='buy'),
    path('toggle/<slug:item_slug>/', views.toggle_item, name='toggle'),
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='myapp/password_reset.html',
            email_template_name='myapp/password_reset_email.html',
            success_url=reverse_lazy('profile_app:password_reset_done'),
            from_email = "noreply@example.com"
        ),
        name='password_reset'
    ),

    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='myapp/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='myapp/password_reset_confirm.html',
            success_url=reverse_lazy('profile_app:password_reset_complete')
        ),
        name='password_reset_confirm'
    ),

    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='myapp/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]
