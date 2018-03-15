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
    # Blank labShare URL goes to the intro page
    url(r'^$', views.enter, name = "enter"),
    url(r'^profile/$', views.profileRedirect, name="profileRedirect"),
    url(r'^profile/(?P<username>\w+)/$', views.profile, name='profile'),
    url(r'^profile/(?P<username>\w+)/friendsList$', views.friendsList, name='friendsList'),
    url(r'^labList/(?P<username>\w+)/$', views.labList, name='labList'),
    url(r'^(?P<course>\w+)/lab(?P<labNumber>\d)/$', views.lab, name='lab'),
    url(r'^enrol/$', views.enrol, name="enrol"),
    url(r'^edit_profile/(?P<username>\w+)/$', views.user_edit, name="edit_profile"),
    url(r'^addFriend/$', views.addFriend, name="addFriend"),

    # THIS IS A TEST URL - DO NOT DELETE YET
    url(r'^lab/$', views.lab, name='lab'),
    url(r'^lab_posts/$', views.post_list, name='lab_posts'),

    # patterns for registration-redux
    url(r'^accounts/register/$', MyRegistrationView.as_view(), name='register'),
    url(r'^accounts/', include ("registration.backends.simple.urls")),

    # profile registration for after user registration (2-parts)
    url(r'^register-profile/', views.register_profile, name="register-profile"),
]
