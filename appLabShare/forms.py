from django import forms

from appLabShare.models import UserProfile

class UserProfileForm (forms.ModelForm):
    # Required form fields
    # isStudent it required but is made this way by having the initial value as true
    isStudent = forms.BooleanField (initial=True, required=False)
    name = forms.CharField (required = True, max_length = 128)

    # Non-required fields
    university = forms.CharField (required = False, max_length = 128)
    degree = forms.CharField (required = False, max_length = 128)
    picture = forms.ImageField (required = False)
    bio = forms.CharField (required = False, max_length = 128)


    class Meta:
        model = UserProfile
        exclude = ("user", "friends", "courses",)
