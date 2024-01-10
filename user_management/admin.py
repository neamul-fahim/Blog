from django.contrib import admin
from . models import CustomUser, OtpVerification

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(OtpVerification)
