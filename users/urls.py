from django.urls import path
from . import views
from .views import UserEditView, UserAccountDeleteView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('signup', views.register_view, name='signup'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('email_activation/<uidb64>/<token>/', views.activate, name='activate'),
    path('edit_profile', UserEditView.as_view(), name='edit_profile'),
    path('edit_profile_pic', views.edit_profile_pic, name='edit_profile_pic'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('reset_password/<uidb64>/<token>/', views.reset_forgotten_password, name='reset_password'),
    path('change_password', views.change_password, name='change_password'),
    path('delete', UserAccountDeleteView.as_view(template_name='users/delete.html'), name='user_delete'),
    #path('edit_profile_pic', views.edit_profile_pic, name='edit_profile_pic'),
    #path('password', auth_views.PasswordChangeView.as_view(template_name='link_to_reset_password.html'), name='change_password'),
    #path('<int:pk>/profile/', views.show_profile_page, name='show_profile_page'),
    path('set_new_email', views.set_new_email, name='set_new_email'),
    #path('<int:pk>/profile', views.edit_profile, name='edit_profile'),
]
