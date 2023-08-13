from django import forms

class NewPost(forms.Form):
    title = forms.CharField(label="Title",max_length=250, widget=forms.TextInput(attrs={'class': 'form-control'}))
    body = forms.CharField(label="Body",widget=forms.Textarea(attrs={'class' : 'form-control'}))