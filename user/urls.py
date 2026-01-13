from django.urls import path
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import CustomPasswordResetView

app_name = 'user'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<int:user_id>/', views.profile_view, name='profile'),
    path('users/', views.users_view, name='users'),
    path('business/edit_business/', views.edit_business, name='edit_business'),
    path('business/edit_profile/<int:user_id>/', views.edit_profile, name='edit_profile'),
    path('business/service/add', views.add_service, name='add_service'),
    path('business/product/add', views.add_product, name='add_product'),
    path('business/service/edit/<int:service_id>/', views.edit_service, name='edit_service'),
    path('business/service/delete/<int:service_id>/', views.delete_service, name='delete_service'),
    path('business/product/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('business/product/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    # Password reset
    path('password-reset/', 
     CustomPasswordResetView.as_view(
         html_email_template_name='user/emails/password_reset_email.html'
     ),
     name='password_reset'),

    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='user/password_reset_done.html'
         ), 
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='user/password_reset_confirm.html',
             success_url='/user/password-reset-complete/'
         ),
         name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='user/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]

    




