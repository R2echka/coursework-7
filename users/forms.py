from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username','email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Придумайте имя пользователя'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Укажите свой email'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Придумайте пароль'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Точно запомнили?'})