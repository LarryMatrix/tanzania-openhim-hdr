from django.urls import path
from UserManagement.views import main

urlpatterns = [
    path('', main.get_login_page, name='login_page'),
    path('password/', main.change_password, name='change_password'),
    path('dashboard', main.get_dashboard, name='dashboard'),
    path('save_changed_password/', main.set_changed_password, name='save_changed_password'),
    path('user', main.authenticate_user, name='authenticate_user'),
    path('accounts/login/', main.change_password, name='login_required_page'),
    path('logout', main.logout_view, name='logout'),
    path('change_password', main.change_password, name='change_password'),

]