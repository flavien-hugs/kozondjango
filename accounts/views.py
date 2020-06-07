# -*- coding: utf-8 -*-

from django.urls import reverse_lazy
from django.contrib.auth import login
from django.views.generic import UpdateView
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from accounts.forms import SignUpForm, UserInfoUpdateForm

# Create your views here.


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()

    context = {'form': form}
    template = 'accounts/signup.html'
    return render(request, template, context)


@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    form_class = UserInfoUpdateForm
    template_name = "accounts/account.html"
    success_url = reverse_lazy('accounts:account')

    def get_object(self):
        return self.request.user
