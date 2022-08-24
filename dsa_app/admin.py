from django.contrib import admin
from .models import *


admin.site.register(UserProfile)
admin.site.register(Question)
admin.site.register(Sheet)
admin.site.register(UserQuestion)
admin.site.register(Solution)
