from django.contrib import admin

from .models import Category, Expertise, Userdata, UserExpertise, Messages, Resume, Portfolio
admin.site.register(Category)
admin.site.register(Expertise)
admin.site.register(Userdata)
admin.site.register(UserExpertise)
admin.site.register(Messages)
admin.site.register(Resume)
admin.site.register(Portfolio)

# Register your models here.
