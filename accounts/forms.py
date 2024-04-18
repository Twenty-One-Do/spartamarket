from django.contrib.auth.forms import UserCreationForm, get_user_model
from django.contrib.auth.models import User
from django import forms
import re

username_pattern = re.compile(r'^[가-힣\s]+$')
email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

class CustomUserCreationForm(UserCreationForm):
    #username = forms.CharField(validators=[])
    class Meta:
        model = get_user_model()
        fields = [
            "email",
            "username",
            "password1",
            "password2",
        ]

    def clean_username(self):
        username=self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("해당 유저네임은 이미 존재합니다!")
        
        if not (2<=len(username)<=10):
            raise forms.ValidationError("유저네임은 2글자 이상 10글자 이하여야 합니다!")

        if not bool(username_pattern.match(username)):
            raise forms.ValidationError("유저네임은 한글로만 작성되어야 합니다!")

        return username

    def clean_email(self):
        email=self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("해당 이메일은 이미 존재합니다!")

        if not bool(email_pattern.match(email)):
            raise forms.ValidationError("이메일에 부적합한 문자가 있습니다!")

        return email

class UserUpdateForm(forms.Form):
    profile = forms.ImageField()
    username = forms.CharField()

    def clean_profile(self):
        image = self.cleaned_data.get('profile')
        if image:
            if image.size > 4*1024*1024:
                raise forms.ValidationError("Image file too large (maximum size is 4MB)")
            return image
        else:
            raise forms.ValidationError("Couldn't read uploaded image")

    def clean_username(self):
        username=self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("해당 유저네임은 이미 존재합니다!")
        
        if not (2<=len(username)<=10):
            raise forms.ValidationError("유저네임은 2글자 이상 10글자 이하여야 합니다!")

        if not bool(username_pattern.match(username)):
            raise forms.ValidationError("유저네임은 한글로만 작성되어야 합니다!")

        return username
