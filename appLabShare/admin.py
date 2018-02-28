from django.contrib import admin

from appLabShare.models import UserProfile, Lab, Course, Post


# class UserProfileAdmin (admin.ModelAdmin):
#     list_display = ()

admin.site.register (UserProfile)
admin.site.register (Lab)
admin.site.register (Course)
admin.site.register (Post)
