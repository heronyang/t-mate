from django import forms

# App
from tmate.models import *

# Django
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.utils.translation import ugettext_lazy as _

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        exclude = ('user', 'picture_url', )
        labels = {}
        help_texts = {
                'user_type': 'User Type',
                }

    image      = forms.FileField(required=False)

    first_name = forms.CharField(max_length=20)
    last_name  = forms.CharField(max_length=20)

    email      = forms.EmailField(max_length = 50,
                                  validators = [validate_email])

    username   = forms.CharField(max_length = 20)

    password1  = forms.CharField(max_length = 200,
                                 label='Password',
                                 widget = forms.PasswordInput())
    password2  = forms.CharField(max_length = 200,
                                 label='Again',
                                 widget = forms.PasswordInput())

    def clean(self):

        cleaned_data = super(ProfileForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data

    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return username

    def clean_image(self):

        image = self.cleaned_data['image']

        if not image:
            # can be optional
            return image
        if not image.content_type or not image.content_type.startswith('image'):
            raise forms.ValidationError('File type is not image')
        if image.size > const.MAX_UPLOAD_SIZE:
            raise forms.ValidationError('File too big (max size is {0} bytes)'.format(const.MAX_UPLOAD_SIZE))
        return image

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        exclude = ('user', 'author', )
        labels = {}
        help_texts = {}
