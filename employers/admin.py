from django.contrib import admin

from employers.models import Report, User, Revenue

admin.site.register(User)
admin.site.register(Report)
admin.site.register(Revenue)

