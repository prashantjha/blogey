from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from models import *
from django.utils.translation import ugettext_lazy as _


class NewPostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title','content',)
        

        labels = {
            'title': _('title'),
            'content': _('content'),

        }

        
class MyRegistrationForm(UserCreationForm):

    email = forms.EmailField(required=True)


    class Meta:
        model = User
        fields = ('username', 'email','password1','password2')

    def save(self, commit=True):
        user = super(MyRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']


        if commit:
            user.save()

        return user

