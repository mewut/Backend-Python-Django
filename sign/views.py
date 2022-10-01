from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .forms import BasicSignupForm


class BaseRegisterView(CreateView):
    model = User
    form_class = BasicSignupForm
    success_url = '/'
    