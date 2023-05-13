from django import forms
#
from applications.users.models import Address
from applications.order.models import Order, PaymentMethod

class PlaceOrderForm(forms.ModelForm):

    first_name= forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'First name*',
                'class': 'rounded border-[#d6d6d6] text-neutral-500 w-11/12'
            }
        )
    )

    last_name= forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Last name*',
                'class': 'rounded border-[#d6d6d6] text-neutral-500 w-11/12'
            }
        )
    )

    phone = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Phone number',
                'class': 'rounded border-[#d6d6d6] text-neutral-500 w-11/12'
            }
        )
    )

    postcode = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Post code/ZIP',
                'class': 'rounded border-[#d6d6d6] text-neutral-500 w-11/12'
            }
        )
    )

    address1 = forms.ModelChoiceField(
        queryset=Address.objects.none(),
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'rounded border-[#d6d6d6] text-neutral-500 w-11/12'
            }
        )
    )
    address2 = forms.ModelChoiceField(
        queryset=Address.objects.none(),
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'rounded border-[#d6d6d6] text-neutral-500 w-11/12'
            }
        )
    )
    payment_method = forms.ModelChoiceField(
        queryset=PaymentMethod.objects.all(),
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'rounded border-[#d6d6d6] text-neutral-500 w-11/12'
            }
        )
    )
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'rounded border-[#d6d6d6] text-neutral-500 w-full',
                'placeholder': 'Additional comments',
            }
        )
    )
    class Meta:
        model = Order
        fields=(
            'first_name',
            'last_name',
            'phone',
            'postcode',
            'address1',
            'address2',
            'payment_method',
            'comment'
        )
    def __init__(self, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address1'].queryset = Address.objects.filter(user__id=user_id)
        self.fields['address2'].queryset = Address.objects.filter(user__id=user_id)

