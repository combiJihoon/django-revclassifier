from django import forms
from .models import UserInput, CrawlResult
from django.core.exceptions import ValidationError


class UserInputForm(forms.ModelForm):
    # temp = forms.CharField(max_length=20, required=False)

    class Meta:
        model = UserInput
        fields = ['restaurant', 'address1', 'address2',
                  'address3', 'temp']
        widgets = {
            'restaurant': forms.TextInput(attrs={
                'placeholder': '맛집 이름을 입력하세요'
            }),
            'address1': forms.TextInput(attrs={
                'placeholder': '맛집 주소의 \'시\'까지 입력하세요'
            }),
            'address2': forms.TextInput(attrs={
                'placeholder': '맛집 주소의 \'구\'까지 입력하세요'
            }),
            'address3': forms.TextInput(attrs={
                'placeholder': '맛집 주소의 \'동\'까지 입력하세요'
            }),
            'temp': forms.TextInput(attrs={
                'placeholder': '원하는 맛집이 이름을 알려주세요'
            })
        }

    def clean_title(self):
        restaurant = self.cleaned_data['restaurant']
        if '*' in restaurant:
            raise ValidationError('*은 포함될 수 없습니다.')
        return restaurant
