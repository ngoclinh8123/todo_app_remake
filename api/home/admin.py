from django.contrib import admin
from .models import Todo, CustomUser

# không thêm cái này trang admin lỗi tùm lum
# https://www.youtube.com/watch?v=8jyyuBaZwVU&t=642s
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(Todo)


# class CustomUserAdmin(UserAdmin):
#     fieldsets = (*UserAdmin.fieldsets, ("Additional Info", {"fields": ("userSignature",)}))

# admin.site.register(CustomUser, CustomUserAdmin)

fields = list(UserAdmin.fieldsets)
fields[1] = ("Personal Info", {"fields": ("first_name", "last_name", "email", "tokenSignature")})
UserAdmin.fieldsets = tuple(fields)
admin.site.register(CustomUser, UserAdmin)
