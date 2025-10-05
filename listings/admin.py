from django.contrib import admin
from .models import Pet
from .models import ContactMessage

# Register your models here.
admin.site.register(Pet)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'subject', 'created_at']
    list_filter = ['created_at']
    search_fields = ['full_name', 'email', 'subject', 'message']
    readonly_fields = ['full_name', 'email', 'subject', 'message', 'created_at']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False