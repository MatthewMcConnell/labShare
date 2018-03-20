from django import forms

from appLabShare.models import UserProfile, Post, Course


class UserProfileForm (forms.ModelForm):
    # Required form fields
    status = forms.CharField (required = True, max_length=7)
    name = forms.CharField (required = True, max_length = 128)

    # Non-required fields
    university = forms.CharField (required = False, max_length = 128)
    degree = forms.CharField (required = False, max_length = 128)
    picture = forms.ImageField (required = False)
    bio = forms.CharField (required = False, max_length = 128)
    facebook = forms.URLField(required = False, max_length = 300)
    instagram = forms.URLField(required = False, max_length = 300)
    twitter = forms.URLField(required = False, max_length = 300)
    linkedIn = forms.URLField(required = False, max_length = 300)
    github = forms.URLField(required = False, max_length = 300)


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
        fields = ('content', 'attachedFile')
        widgets = {
            'content' : forms.TextInput(attrs={'class' : 'commentSubmission', 'placeholder' : "Please enter a comment"}),
        }



class AddFriendForm (forms.Form):
    friend = forms.CharField (required = True)
    # Note: this form does not need a meta class (it actually breaks the form) as we are not creating
    # a model object! Simply adding to a field!
