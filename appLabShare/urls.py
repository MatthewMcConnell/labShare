from django.conf.urls import url
from django.conf.urls import include

from registration.backends.simple.views import RegistrationView

from appLabShare import views




class MyRegistrationView (RegistrationView):
    def getSuccessUrl (self, user):
        # Change this to profile page instead when implemented
        return "/labShare/"



# The initial app url mapping below is just for testing and can be changed
# modified to have better url naming later :)

urlpatterns = [
    #url(r'^$', views.testView, name = "testView"),
    url(r'^$', views.login, name = "login"),
    url(r'signup/^$', views.signUp, name = "signup"),




    # patterns for registration-redux
    url(r'^accounts/register/$', MyRegistrationView.as_view(), name='register'),
    url(r'^accounts/', include ("registration.backends.simple.urls")),


    # These are to be uncommented when the views are implemented

    # # url(r'^login/$', views.user_login, name='login')
    # # url(r'^signup/$', views.user_signup, name='login')
    # url(r'^profile/$', views.profile, name='profile')
    #     #r'^profile/$' needs to be dynamic
    # url(r'labs/$', views.labs, name='labs')
]
