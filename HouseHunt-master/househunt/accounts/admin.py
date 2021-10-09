from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import MyUserCreationForm, MyUserChangeForm
from .models import Accountuser,Property,Image,Video,Review
class MyUserAdmin(UserAdmin):
    add_form = MyUserCreationForm
    form = MyUserChangeForm
    model = Accountuser
    list_display = ['username','email','phonenum']
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('phonenum',)}),
    )
admin.site.register(Accountuser, MyUserAdmin)
admin.site.register(Property)
admin.site.register(Image)
admin.site.register(Video)
admin.site.register(Review)
