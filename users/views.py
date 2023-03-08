from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import FormView, UpdateView

from users.forms import SignUpForm, SignInForm
from users.models import User


@login_required(login_url='login')
def sign_out(request):
    logout(request)
    return redirect('/')


class SignUpView(FormView):
    form_class = SignUpForm
    template_name = "users/signup.html"
    success_url = '/'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        login(self.request, user)
        return redirect(self.success_url)


class LogInView(FormView):
    form_class = SignInForm
    template_name = "users/login.html"
    success_url = '/'

    def form_valid(self, form):
        print(self.get_form_kwargs())
        user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])
        login(self.request, user)
        return redirect(self.success_url)


def profile(request):
    return render(request, "main/user_profile.html", {})


class ProfileView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    fields = ('username', 'email', 'avatar')
    model = User
    template_name = 'users/user_profile.html'
    success_url = '../'
