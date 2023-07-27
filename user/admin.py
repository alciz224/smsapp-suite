from django.contrib import admin

# Register your models here.
from user.models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):


    def get_form(self, request, obj=None, **kwargs):
        form=super().get_form(request, obj, **kwargs)
        form.base_fields['username'].required=False
        return form

admin.site.register(CustomUser, CustomUserAdmin)