from typing import Any, Dict
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.html import strip_tags
from django.views.generic import FormView, TemplateView
from django.views import View
#
from .forms import (
        ActivateAccountForm,
        LoginForm, 
        NewAddressForm,
        RecoverPasswordRequestForm,
        RegisterForm, 
        UpdatePasswordForm,
        UpdateInformationForm
    )
from helpers.generate_code import code_generator
from .models import User, Address

""" ************************Authentication************************ """

class RegisterView(FormView):

    form_class = RegisterForm

    template_name = 'authentication/register.html'

    def get(self, request, *args, **kwargs):

        if(self.request.user.is_authenticated):
            return redirect('/')
        else:
            return render(request,self.template_name,{'form': self.form_class})
    
    def form_valid(self, form):

        code = code_generator()

        user = User.objects.create_user(
            form.cleaned_data['email'],
            form.cleaned_data['password'],
            full_name=form.cleaned_data['full_name'],
            token=code
        )

        # send confirmation email
        subject = 'Confirmation Account'
        message = 'Activate your account with the following token: '+code
        sender = settings.EMAIL_SENDER
        send_mail(subject, message, sender, {form.cleaned_data['email'],})

        return HttpResponseRedirect(
            reverse(
                'auth:activate-account',
                kwargs={'token': code}
            )
        )

class ActivateAccount(FormView):

    form_class = ActivateAccountForm

    success_url = reverse_lazy('auth:login')

    template_name = 'authentication/activate_account.html'

    def get(self, request, *args, **kwargs):
        if(self.request.user.is_authenticated):
            return redirect('/')
        else:
            token = self.kwargs['token']
            user = User.objects.filter(token=token).first()
            if user is None:
                return render(request, 'authentication/error.html')
            else:
                return render(request, self.template_name, {'form': self.form_class})
    
    def form_valid(self, form):

        # activate account
        user = User.objects.filter(token=form.cleaned_data['token']).first()

        user.token = None
        user.is_active = True
        user.save()

        return super(ActivateAccount, self).form_valid(form)



class LoginView(FormView):
    form_class = LoginForm
    template_name = 'authentication/login.html'
    success_url = reverse_lazy('home_app:home')

    def get(self, request, *args, **kwargs):

        if self.request.user.is_authenticated:
            return redirect('/')
        
        return render(request, self.template_name, {'form': self.form_class})
    
    def form_valid(self, form):

        # authenticate user
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        user = authenticate(username=email, password=password)

        login(self.request, user)

        return super(LoginView, self).form_valid(form)

class LogoutView(View):

    def get(self, request, *args, **kwargs):
        logout(self.request)
        return redirect('/auth/login')

class RecoverPasswordRequestView(FormView):

    template_name = 'authentication/recover_password.html'
    form_class = RecoverPasswordRequestForm

    def get(self, request, *args, **kwargs):
        if(self.request.user.is_authenticated):
            return redirect('/')
        return render(request, self.template_name, {'form': self.form_class})
    
    def form_valid(self, form):

        # generate new code and send email
        user = User.objects.filter(email=form.cleaned_data['email']).first()

        token = code_generator()

        user.token = token

        user.save()

        subject = 'Update Password'
        html_message = render_to_string('emails/recover_password.html',{'url':settings.BASE_SERVER_URL+'auth/update-password/'+token})
        plain_message = strip_tags(html_message)
        sender = settings.EMAIL_SENDER
        receiver = form.cleaned_data['email']
        send_mail(subject, plain_message, sender, [receiver], html_message=html_message)

        return HttpResponseRedirect(
            reverse(
                'auth:update-password',
                kwargs={'token': token}
            )
        )

class UpdatepasswordView(FormView):

    template_name = 'authentication/update_password.html'
    form_class = UpdatePasswordForm

    def get(self, request, *args, **kwargs):
        if(self.request.user.is_authenticated):
            return redirect('/')
        token = self.kwargs['token']

        user = User.objects.filter(token=token).first()

        if user is None:
            return render(request, 'authentication/error.html')
        
        return render(request, self.template_name, {'form': self.form_class})
    
    def form_valid(self, form):

        # find user
        user = User.objects.filter(
            token=self.kwargs['token']
        ).first()

        # update user
        password = form.cleaned_data['password']

        user.set_password(password)
        user.token = None
        user.save()

        return redirect('/auth/login')

""" ************************User Account************************ """

class UserAccountView(LoginRequiredMixin,TemplateView):

    template_name = 'account/dashboard.html'
    login_url = '/auth/login'
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['user_information'] = User.objects.values('email', 'full_name').get(id=self.request.user.id)
        context['addresses'] = Address.objects.filter(user=self.request.user).order_by('-id')[:1]
        return context

class AccountInformationView(FormView):

    form_class = UpdateInformationForm
    template_name = 'account/account_information.html'

    def get(self, request, *args, **kwargs):

        if(self.request.user.is_anonymous):
            return redirect('/')
        
        return render(request, self.template_name, {'form': self.form_class, 'user': self.request.user})

    def form_valid(self, form):
        
        user = User.objects.get(id=self.request.user.id)

        user.email = form.cleaned_data['email']
        user.full_name = form.cleaned_data['full_name']
        user.save()

        return HttpResponseRedirect(reverse('auth:user-account'))

class AddShippingAddressView(FormView):

    form_class = NewAddressForm
    template_name = 'account/add_address.html'

    def get(self, request, *args, **kwargs):

        if(self.request.user.is_anonymous):
            return redirect('/')
        return render(request, self.template_name, {'form': self.form_class})

    def form_valid(self, form):

        user = User.objects.get(id=self.request.user.id)

        new_address = Address()
        new_address.user = user
        new_address.default_address = form.cleaned_data['default_address']
        new_address.default_shipping_address = form.cleaned_data['default_shipping_address']
        new_address.save()

        return HttpResponseRedirect(reverse('auth:user-account'))

class AllUsersView(View):

    template_name = 'users/all_users.html'

    def get(self, request, *args, **kwargs):

        if(self.request.user.is_anonymous):
            return redirect('/')
        
        users = User.objects.all()
        paginator = Paginator(users, 6)
        page = self.request.GET.get('page')
        obj_page = paginator.get_page(page)
        return render(request, self.template_name, {'page_obj': obj_page})

class DisableUser(View):

    def post(self, request, *args, **kwargs):

        if(self.request.user.is_anonymous or self.request.user.ocupation != '0'):
            return redirect('/')

        user_id = self.request.POST.get('user_id')

        user = User.objects.get(id=user_id)

        user.is_active = False
        user.save()
        return redirect('auth:all-users')
    
class EnableUser(View):

    def post(self, request, *args, **kwargs):

        if(self.request.user.is_anonymous or self.request.user.ocupation != '0'):
            return redirect('/')

        user_id = self.request.POST.get('user_id')

        user = User.objects.get(id=user_id)

        user.is_active = True
        user.save()
        return redirect('auth:all-users')









