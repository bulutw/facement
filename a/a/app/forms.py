from django import forms
from django.forms import ModelForm, ModelChoiceField, ModelMultipleChoiceField
from creditcards.forms import CardNumberField, CardExpiryField, SecurityCodeField

from .models import Card, Item

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from creditcards.forms import CardNumberField, CardExpiryField, SecurityCodeField

class LoginForm(forms.Form):
	username = forms.CharField(max_length = 25, label = 'USERNAME')
	password = forms.CharField(max_length = 25, label = 'PASSWORD', widget = forms.PasswordInput)

	def clean(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')

		if username and password:
			user = authenticate(username = username, password = password)
			if not user:
				raise forms.ValidationError('Hatalı giriş.')

		return super(LoginForm, self).clean()

class RegisterForm(forms.ModelForm):
	username = forms.CharField(max_length = 25, label = 'USERNAME')
	password = forms.CharField(max_length = 25, label = 'PASSWORD', widget = forms.PasswordInput)
	password_again = forms.CharField(max_length = 25, label = 'PASSWORD AGAIN', widget = forms.PasswordInput)

	class Meta:
		model = User
		fields = ['username', 'password', 'password_again',]

	def clean_password_again(self):
		password = self.cleaned_data.get('password')
		password_again = self.cleaned_data.get('password_again')

		if password and password_again and password != password_again:
			raise forms.ValidationError('Parolalar eşleşmiyor!')

		return password_again

class CreateCard(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['card_number', 'card_exp', 'card_sec', 'name_on_card']

class CardCheck(forms.Form):
	card_num = CardNumberField()
	client_id = forms.CharField(max_length = 29)

class PaymentForm(forms.Form):
    cc_number = CardNumberField(label='Card Number')
    cc_expiry = CardExpiryField(label='Expiration Date')
    cc_code = SecurityCodeField(label='CVV/CVC')
	

    
