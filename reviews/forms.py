from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['restaurant', 'address']
        widgets = {
            'restaurant': forms.TextInput(attrs={
                'placeholder': '맛집 이름을 입력하세요'
            }),
            'address': forms.TextInput(attrs={
                'placeholder': '맛집 주소의 \'동\'까지 입력하세요(예시 : 서울시 강남구 대치동)'
            })
        }
