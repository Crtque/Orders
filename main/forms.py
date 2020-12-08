from django import forms
from .models import *

class LoginForm(forms.Form):
	login = forms.CharField(label="Логин", required=True, widget = forms.TextInput(attrs={'placeholder': "Введите ваш логин..."}), max_length=50 )
	password = forms.CharField(label="Пароль", required=True, widget=forms.PasswordInput(attrs={'placeholder': "Введите ваш пароль..."}), max_length=150)

class UserAddingForm(forms.Form):
	username = forms.CharField(label="Логин", required=True, widget = forms.TextInput(attrs={'placeholder': "Логин пользователя..."}), max_length=50)
	password = forms.CharField(label="Пароль", required=True, widget=forms.PasswordInput(attrs={'placeholder': "Пароль пользователя..."}), max_length=150)
	group = forms.ChoiceField(label="Группа бзопасности", widget = forms.Select(), choices = ([('Заказчик','Заказчик'), ('Организация','Организация'),('Модератор','Модератор'), ]), required = True)

class OrgAddingForm(forms.Form):
	name = forms.CharField(label="Название организации (Логин)", required=True, widget = forms.TextInput(attrs={'placeholder': ""}), max_length=50)
	date = forms.CharField(label="Дата основания", required=True, widget=forms.TextInput(attrs={'placeholder': ""}), max_length=150)
	dirname = forms.CharField(label="ФИО Директора", required=True,  widget=forms.TextInput(attrs={'placeholder': ""}), max_length=50)
	dob = forms.CharField(label="Дата рождения директора", required=True,   widget=forms.TextInput(attrs={'placeholder': ""}), max_length=50)

class CreationForm(forms.Form):
	info = forms.CharField(label="Информация", required=True, widget = forms.TextInput(attrs={'placeholder': ""}), max_length=50)
	expecting = forms.CharField(label="Ожидаемая дата", required=True, widget=forms.TextInput(attrs={'placeholder': ""}), max_length=150)
