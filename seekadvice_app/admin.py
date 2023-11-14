from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, ServiceTechnology, ServiceAreas,  ServiceOffer, ServiceOfferTechExpert, ServiceAreasTechExpert

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser)
#admin.site.register(CustomUserAdmin)
# Register your models here.
admin.site.register(ServiceTechnology)
admin.site.register(ServiceAreas)
admin.site.register(ServiceOffer)
admin.site.register(ServiceOfferTechExpert)
admin.site.register(ServiceAreasTechExpert)