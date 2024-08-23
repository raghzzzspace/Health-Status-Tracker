from django.contrib import admin
from .models import SignUp, Profile, Exercise, BP, Water, Weight, Sleep

# Register your models here.
admin.site.register(SignUp)
admin.site.register(Profile)
admin.site.register(Exercise)
admin.site.register(BP)
admin.site.register(Water)
admin.site.register(Weight)
admin.site.register(Sleep)