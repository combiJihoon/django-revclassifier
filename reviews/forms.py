from django import forms
from .models import Review
from django.core.exceptions import ValidationError


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['restaurant', 'address1', 'address2', 'address3']
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
            })
        }

    def clean_title(self):
        restaurant = self.cleaned_data['restaurant']
        if '*' in restaurant:
            raise ValidationError('*은 포함될 수 없습니다.')
        return restaurant
