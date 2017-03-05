from django import forms

class ApplicationForm(forms.Form):
	body = forms.CharField(widget=forms.Textarea)