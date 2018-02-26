from django.conf.urls import url

from appLabShare import views


# The initial app url mapping below is just for testing and can be changed
# modified to have better url naming later :)

urlpatterns = [
    url(r'^$', views.testView, name = "testView")
    url(r'^login/$', views.user_login, name='login')
    url(r'^signup/$', views.user_signup, name='login')
    url(r'^profile/$', views.profile, name='profile')
        #r'^profile/$' needs to be dynamic
    url(r'labs/$', views.labs, name='labs')
]
