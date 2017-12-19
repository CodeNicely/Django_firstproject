from django.contrib import admin

# Register your models here.
from student.models import user_data


class user_dataAdmin(admin.ModelAdmin):
    list_display = ['username', 'mobile', 'password']


admin.site.register(user_data, user_dataAdmin)
