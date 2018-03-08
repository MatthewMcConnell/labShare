from django import forms

from appLabShare.models import UserProfile

class UserProfileForm (forms.ModelForm):
    # Required form fields
    isStudent = forms.BooleanField (required = True)

    # Non-required fields
    picture = forms.ImageField (required = False)
    bio = forms.CharField (required = False, max_length = 128)
    degree = forms.CharField (required = False, max_length = 128)


    class Meta:
        model = UserProfile
        exclude = ("user", "friends", "courses",)
