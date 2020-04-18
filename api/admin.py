from __future__ import unicode_literals
from django.contrib import admin
from .models import User
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.

class UserAdmin(BaseUserAdmin):
    list_display = ( 'name', 'phone','admin','email',)
    list_filter = ('staff','active','admin',)
    fieldsets  = (
        (None, {'fields':('phone','password',)}),
        ('Personal_info',{'fields':('name','email',)}),
        ('Permissions', {'fields':('admin','staff','active',)}),
    )

    add_fieldsets = (
        (None, {
            'classes':('wide',),
            'fields':('phone','password')
        }),
    )

    search_fields = ('phone','name')
    ordering = ('phone','name')
    filter_horizontal = ()

    def get_inline_instances(self,request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(Group)
admin.site.register(User, UserAdmin)


