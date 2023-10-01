from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm
from .models import *

# Register your models here.
@admin.register(Storage)
class CandidateInfoAdmin(admin.ModelAdmin):
    search_fields = ('user',)
    list_display=[field.name for field in Storage._meta.get_fields()]

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Other Personal info',
            {
                'fields': (
                    'random_string',
                )
            }
        )
    )


admin.site.register(CustomUser, CustomUserAdmin)