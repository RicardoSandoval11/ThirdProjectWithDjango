from django import forms
#
from .models import Category

class CreateCategoryForm(forms.ModelForm):

    name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'label': 'Category name',
                'placeholder': 'Category name',
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
                'placeholder': 'Brief description about the category',
                'class': 'border-[#f1f1f1] w-full rounded-md border bg-[#FCFDFE] py-3 px-5 text-base text-body-color placeholder-[#ACB6BE] outline-none focus:border-primary focus-visible:shadow-none'
            }
        )
    )

    class Meta:
        model = Category
        fields = (
            'name',
            'image',
            'description'
        )