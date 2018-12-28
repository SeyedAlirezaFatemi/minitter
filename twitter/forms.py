from captcha.fields import ReCaptchaField
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    name = forms.CharField(max_length=30, help_text='Shown to other users.')
    email = forms.EmailField(max_length=254, help_text='No user has access to your email address.')

    class Meta:
        model = User
        fields = ('username', 'name', 'email', 'password1', 'password2',)


# class UserAvatarForm(forms.Form):
#     avatar = forms.ImageField()
#
#     class Meta:
#         model = Profile
#
#     def clean_avatar(self):
#         avatar = self.cleaned_data['avatar']
#
#         try:
#             w, h = get_image_dimensions(avatar)
#
#             # Validate dimensions
#             max_width = max_height = 1000
#             if w > max_width or h > max_height:
#                 raise forms.ValidationError(
#                     f'Please use an image that is {max_width} x {max_height} pixels or smaller.')
#
#             # Validate content type
#             main, sub = avatar.content_type.split('/')
#             if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
#                 raise forms.ValidationError('Please use a JPEG, GIF or PNG image.')
#
#             # Validate file size
#             if len(avatar) > (20 * 1024 * 1024):
#                 raise forms.ValidationError('Avatar file size may not exceed 20m.')
#
#         except AttributeError:
#             """
#             Handles case when we are updating the user profile
#             and do not supply a new avatar
#             """
#             pass
#
#         return avatar

class ImageUploadForm(forms.Form):
    avatar = forms.ImageField()
