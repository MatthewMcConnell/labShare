from django.conf.urls import url
from django.conf.urls import include
from django.urls import reverse

from registration.backends.simple.views import RegistrationView

from appLabShare import views


# This is to modify the registration-redux flow to redirect to the profile setup page
# once they successfully set up the main user (user model)
class MyRegistrationView (RegistrationView):
    def get_success_url (self, user):
        return reverse ("register-profile")


urlpatterns = [
    # url's for initial welcome and login
    url(r'^$', views.enter, name = "enter"),
    url(r'^profile/$', views.profileRedirect, name="profileRedirect"),

    # url's for viewing a users infor
    url(r'^profile/(?P<username>\w+)/$', views.profile, name='profile'),
    url(r'^friendsList/(?P<username>\w+)/$', views.friendsList, name='friendsList'),
    url(r'^labList/(?P<username>\w+)/$', views.labList, name='labList'),

    # url's to add, edit and participate in certain parts of the website
    url(r'^(?P<course>\w+)/lab(?P<labNumber>\d+)/$', views.lab, name='lab'),
    url(r'^enrol/$', views.enrol, name="enrol"),
    url(r'^edit_profile/$', views.editProfile, name="edit_profile"),
    url(r'^addFriend/$', views.addFriend, name="addFriend"),

    # patterns for registration-redux
    url(r'^accounts/register/$', MyRegistrationView.as_view(), name='register'),
    url(r'^accounts/', include ("registration.backends.simple.urls")),

    # profile registration for after user registration (part 1 = user, part 2 = profile)
    url(r'^register-profile/', views.register_profile, name="register-profile"),
]
