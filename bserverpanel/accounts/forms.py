from django import forms

class RegisterPanelUserForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(max_length=255, required=True)
    password = forms.CharField(max_length=255, required=True, widget=forms.PasswordInput)
    password_confirm = forms.CharField(max_length=255, required=True, widget=forms.PasswordInput)

class LoginPanelUserForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput)