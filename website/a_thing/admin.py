from django.contrib import admin
from .models import Family, Person
from .models import Profile

# Register your models here.
admin.site.register(Family)
admin.site.register(Person)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']

