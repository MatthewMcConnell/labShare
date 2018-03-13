from django import forms

from appLabShare.models import UserProfile, Post


class UserProfileForm (forms.ModelForm):
    # Required form fields
    # status it required but is made this way by having the initial value as true
    status = forms.CharField (required = True, max_length=7)
    name = forms.CharField (required = True, max_length = 128)

    # Non-required fields
    university = forms.CharField (required = False, max_length = 128)
    degree = forms.CharField (required = False, max_length = 128)
    picture = forms.ImageField (required = False)
    bio = forms.CharField (required = False, max_length = 128)


    class Meta:
        model = UserProfile
        exclude = ("user", "friends", "courses",)



class EnrolForm (forms.Form):
    course = forms.CharField (required = True, max_length=128)
    level = forms.IntegerField (required = True, min_value=1, max_value=10)
    labNumber = forms.IntegerField (required = True, min_value=1, max_value=20)



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content',)
