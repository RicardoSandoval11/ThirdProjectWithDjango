from django import forms
from django.contrib.auth import authenticate
#
from .models import User

class RegisterForm(forms.ModelForm):

    email = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'label': 'Email',
                'placeholder': 'email',
                'class': 'border-[#E9EDF4] w-full rounded-md border bg-[#FCFDFE] py-3 px-5 text-base text-body-color placeholder-[#ACB6BE] outline-none focus:border-primary focus-visible:shadow-none'
            }
        )
    )

    full_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'label': 'Full Name',
                'placeholder': 'Your name',
                'class': 'border-[#E9EDF4] w-full rounded-md border bg-[#FCFDFE] py-3 px-5 text-base text-body-color placeholder-[#ACB6BE] outline-none focus:border-primary focus-visible:shadow-none'
            }
        )
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'label': 'Password',
                'placeholder': 'Password',
                'class': 'border-[#E9EDF4] w-full rounded-md border bg-[#FCFDFE] py-3 px-5 text-base text-body-color placeholder-[#ACB6BE] outline-none focus:border-primary focus-visible:shadow-none'
            }
        )
    )

    password_confirmation = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'label': 'Confirm_password',
                'placeholder': 'Password confirmation',
                'class': 'border-[#E9EDF4] w-full rounded-md border bg-[#FCFDFE] py-3 px-5 text-base text-body-color placeholder-[#ACB6BE] outline-none focus:border-primary focus-visible:shadow-none'
            }
        )
    )

    class Meta:
        model = User
        fields = (
            'email',
            'full_name',
            'password',
            'password_confirmation'
        )

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).first()
        if user is not None:
            self.add_error('email', 'User with this email already exists')
        return email
    
    def clean_password(self):
        password = self.cleaned_data['password']
        password_confirmation = self.data['password_confirmation']
        if(password != password_confirmation):
            self.add_error('password', 'Passwords are different')
        return password

class ActivateAccountForm(forms.Form):

    token = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'label': 'Activation token',
                'placeholder': 'Your token',
                'class': 'border-[#E9EDF4] w-full rounded-md border bg-[#FCFDFE] py-3 px-5 text-base text-body-color placeholder-[#ACB6BE] outline-none focus:border-primary focus-visible:shadow-none'
            }
        )
    )

    def clean_token(self):
        token = self.cleaned_data['token']
        user = User.objects.filter(
            token=token
        ).first()
        if user is None:
            self.add_error('token', 'Invalid token')
        return token

class LoginForm(forms.Form):

    email = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'label': 'Email',
                'placeholder': 'email',
                'class': 'border-[#E9EDF4] w-full rounded-md border bg-[#FCFDFE] py-3 px-5 text-base text-body-color placeholder-[#ACB6BE] outline-none focus:border-primary focus-visible:shadow-none'
            }
        )
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'label': 'Password',
                'placeholder': 'Password',
                'class': 'border-[#E9EDF4] w-full rounded-md border bg-[#FCFDFE] py-3 px-5 text-base text-body-color placeholder-[#ACB6BE] outline-none focus:border-primary focus-visible:shadow-none'
            }
        )
    )

    def clean(self):

        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        if not authenticate(username=email, password=password):
            self.add_error('email', 'Wrong Credentials')
        
        return self.cleaned_data

class RecoverPasswordRequestForm(forms.Form):

    email = forms.CharField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                'label': 'Email',
                'placeholder': 'Your email',
                'class': 'border-[#E9EDF4] w-full rounded-md border bg-[#FCFDFE] py-3 px-5 text-base text-body-color placeholder-[#ACB6BE] outline-none focus:border-primary focus-visible:shadow-none'
            }
        )
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).first()
        if user is None:
            self.add_error('email', 'User with this email does not exist')
        return email

class UpdatePasswordForm(forms.Form):

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'label': 'Password',
                'placeholder': 'Password',
                'class': 'border-[#E9EDF4] w-full rounded-md border bg-[#FCFDFE] py-3 px-5 text-base text-body-color placeholder-[#ACB6BE] outline-none focus:border-primary focus-visible:shadow-none'
            }
        )
    )

    password_confirmation = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'label': 'Confirm password',
                'placeholder': 'Confirm password',
                'class': 'border-[#E9EDF4] w-full rounded-md border bg-[#FCFDFE] py-3 px-5 text-base text-body-color placeholder-[#ACB6BE] outline-none focus:border-primary focus-visible:shadow-none'
            }
        )
    )

    def clean_password(self):
        password = self.data['password']
        password_confirmation = self.data['password_confirmation']
        if(password != password_confirmation):
            self.add_error('password', 'Passwords are different')
            
        return password

class UpdateInformationForm(forms.Form):

    id = forms.CharField(
        required=True,
        widget=forms.HiddenInput()
    )
    
    full_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'label': 'Name',
                'class': 'border-[#f1f1f1] w-full rounded-md border bg-[#FCFDFE] py-3 px-5 text-base text-body-color placeholder-[#ACB6BE] outline-none focus:border-primary focus-visible:shadow-none'
            }
        )
    )

    email = forms.CharField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                'label': 'Email',
                'class': 'border-[#f1f1f1] w-full rounded-md border bg-[#FCFDFE] py-3 px-5 text-base text-body-color placeholder-[#ACB6BE] outline-none focus:border-primary focus-visible:shadow-none'
            }
        )
    )

    def clean_email(self):
        user_id = self.cleaned_data['id']
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).first()
        if user is not None and int(user_id) != user.id:
            self.add_error('email', 'This email is already in use')
        return email 

class NewAddressForm(forms.Form):

    default_address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'label': 'Default address',
                'placeholder': 'Default address',
                'class': 'border-[#f1f1f1] w-full rounded-md border bg-[#FCFDFE] py-3 px-5 text-base text-body-color placeholder-[#ACB6BE] outline-none focus:border-primary focus-visible:shadow-none'
            }
        )
    )

    default_shipping_address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'label': 'Default shipping address',
                'placeholder': 'Default shipping address',
                'class': 'border-[#f1f1f1] w-full rounded-md border bg-[#FCFDFE] py-3 px-5 text-base text-body-color placeholder-[#ACB6BE] outline-none focus:border-primary focus-visible:shadow-none'
            }
        )
    )

    def clean_default_address(self):
        default_address = self.cleaned_data['default_address']
        if(len(default_address.strip()) == 0):
            self.add_error('default_address', 'Default address field is required')
        return default_address
    
    def clean_default_shipping_address(self):
        default_shipping_address = self.cleaned_data['default_shipping_address']
        if(len(default_shipping_address.strip()) == 0):
            self.add_error('default_shipping_address', 'Default shipping address field is required')
        return default_shipping_address
