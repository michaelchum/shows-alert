from django import forms
from episodes.models import TvShows, UserProfile
from django.contrib.auth.models import User

def clean(self):
	cleaned_data = self.cleaned_data
	url = cleaned_data.get('url')
	# If url is not empty and doesn't start with 'http://' add 'http://' to the beginning.
	if url and not url.startswith('http://'):
		url = 'http://' + url
		cleaned_data['url'] = url

	return cleaned_data

class UserForm(forms.ModelForm):
	username = forms.CharField(help_text="Please enter a username.")
	email = forms.CharField(help_text="Please enter your email.")
	password = forms.CharField(widget=forms.PasswordInput(), help_text="Please enter a password.")

	class Meta:
		model = User
		fields = ['username', 'email', 'password']

class UserProfileForm(forms.ModelForm):
	website = forms.URLField(help_text="Please enter your website.", required=False)
	picture = forms.ImageField(help_text="Select a profile image to upload.", required=False)

	class Meta:
		model = UserProfile
		fields = ['website', 'picture']