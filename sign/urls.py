from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import BaseRegisterView, Update_profile, BaseRegisterView, Account, add_authors

urlpatterns = [
    path('account/', Account.as_view()),
    path('login/', LoginView.as_view(template_name = 'sign/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name = 'sign/logout.html'), name='logout'),
    path('signup/', BaseRegisterView.as_view(template_name = 'sign/signup.html'), name='signup'),
    path('add_authors/', add_authors, name = 'upgrade'),

]




