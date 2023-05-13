from django import forms
#
from applications.categories.models import Category
from .models import Book

class CreateBookForm(forms.ModelForm):

    IS_OFFER_OPTIONS = (
        (True, 'Yes'),
        (False, 'No')
    )

    name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'label': 'Name',
                'placeholder': 'Name of the book',
                'class': 'border-[#f1f1f1] w-full rounded-md border bg-[#FCFDFE] py-3 px-5 text-base text-body-color placeholder-[#ACB6BE] outline-none focus:border-primary focus-visible:shadow-none'
            }
        )
    )

    purchase_price = forms.DecimalField(
        required=True,
        widget=forms.NumberInput(
            attrs={
                'label': 'Purchase price',
                'placeholder': 'Purchase price',
                'class': 'border-[#f1f1f1] w-full rounded-md border bg-[#FCFDFE] py-3 px-5 text-base text-body-color placeholder-[#ACB6BE] outline-none focus:border-primary focus-visible:shadow-none'
            }
        )
    )

    sell_price = forms.DecimalField(
        required=True,
        widget=forms.NumberInput(
            attrs={
                'label': 'Purchase price',
                'placeholder': 'Normal sell price',
                'class': 'border-[#f1f1f1] w-full rounded-md border bg-[#FCFDFE] py-3 px-5 text-base text-body-color placeholder-[#ACB6BE] outline-none focus:border-primary focus-visible:shadow-none'
            }
        )
    )

    offer_price = forms.DecimalField(
        required=True,
        widget=forms.NumberInput(
            attrs={
                'label': 'Purchase price',
                'placeholder': 'Offer price',
                'class': 'border-[#f1f1f1] w-full rounded-md border bg-[#FCFDFE] py-3 px-5 text-base text-body-color placeholder-[#ACB6BE] outline-none focus:border-primary focus-visible:shadow-none'
            }
        )
    )

    is_offer = forms.ChoiceField(
        required=True,
        choices=IS_OFFER_OPTIONS,
        widget=forms.Select(
            attrs={
                'label': 'Is Offer?',
                'class': 'border-[#f1f1f1] w-9/12 rounded-md border bg-[#FCFDFE] py-3 px-5 text-base text-body-color placeholder-[#ACB6BE] outline-none focus:border-primary focus-visible:shadow-none'
            },
        )
    )

    stock = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(
            attrs={
                'label': 'Available products',
                'placeholder': 'Stock',
                'class': 'border-[#f1f1f1] w-full rounded-md border bg-[#FCFDFE] py-3 px-5 text-base text-body-color placeholder-[#ACB6BE] outline-none focus:border-primary focus-visible:shadow-none'
            }
        )
    )

    author = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'label': 'Author',
                'placeholder': 'Author',
                'class': 'border-[#f1f1f1] w-full rounded-md border bg-[#FCFDFE] py-3 px-5 text-base text-body-color placeholder-[#ACB6BE] outline-none focus:border-primary focus-visible:shadow-none'
            }
        )
    )

    image = forms.ImageField(
        required=True,
        widget=forms.FileInput(
            attrs={
                'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none'
            }
        )
    )

    description = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Description',
                'class': 'border-[#f1f1f1] w-full rounded-md border bg-[#FCFDFE] py-3 px-5 text-base text-body-color placeholder-[#ACB6BE] outline-none focus:border-primary focus-visible:shadow-none'
            }
        )
    )

    details = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Details',
                'class': 'border-[#f1f1f1] w-full rounded-md border bg-[#FCFDFE] py-3 px-5 text-base text-body-color placeholder-[#ACB6BE] outline-none focus:border-primary focus-visible:shadow-none'
            }
        )
    )

    category = forms.ModelChoiceField(
        required=True,
        queryset=Category.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'border-[#f1f1f1] w-9/12 rounded-md border bg-[#FCFDFE] py-3 px-5 text-base text-body-color placeholder-[#ACB6BE] outline-none focus:border-primary focus-visible:shadow-none'
            }
        )
    )

    class Meta:
        model = Book
        fields = [
            'name',
            'description',
            'purchase_price',
            'sell_price',
            'is_offer',
            'offer_price',
            'details',
            'stock',
            'category',
            'author',
            'image'
        ]
    
    
    def clean(self):
        cleaned_data = super(CreateBookForm, self).clean()

        #sell price validation
        sell_price = self.cleaned_data['sell_price']
        if(sell_price < 0):
            self.add_error('sell_price', 'Sell price cannot be less than zero')
    
        # offer price valdiation
        is_offer = self.cleaned_data['is_offer']
        if(is_offer):
            offer_price = self.cleaned_data['offer_price']
            if(offer_price is None):
                self.add_error('offer_price', 'If is offer field is selected, a offer price must be set')
            if(offer_price < 0):
                self.add_error('offer_price', 'Offer price cannot be less than zero')

        # purcahse price validation
        purchase_price = self.cleaned_data['purchase_price']
        sell_price = self.cleaned_data['sell_price']
        is_offer = self.cleaned_data['is_offer']
        offer_price = self.cleaned_data['offer_price']
        if(purchase_price > sell_price):
            self.add_error('purchase_price', 'Purchase price is greater than sell price')
        if(is_offer):
            if(offer_price > sell_price):
                self.add_error('offer_price', 'Purchase price is greater than offer price')
        if(purchase_price < 0):
            self.add_error('purchase_price', 'Purchase price cannot be less than zero')
        
        # stock field valdiation
        stock = self.cleaned_data['stock']
        if(stock < 0):
            self.add_error('stock', 'Stock cannot be less than zero')

        return cleaned_data