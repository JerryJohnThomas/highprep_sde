from django.contrib import admin
from .models import PersonInfo
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin;


# Register your models here.
# admin.site.register(PersonInfo)


class UserModelAdmin(BaseUserAdmin):
   

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id', 'name', 'email', 'phone_number', 'age', 'person_type', 'bike_details','is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        ('UserCredentials', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name','phone_number', 'age')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )


    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ( 'name', 'email', 'phone_number', 'age', 'person_type', 'bike_details','password', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email','id')
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(PersonInfo, UserModelAdmin)