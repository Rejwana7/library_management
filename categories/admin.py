from django.contrib import admin

# Register your models here.

from . import models

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields ={'slug': ('name',)}
    list_display= ['name','slug']

admin.site.register(models.Category,CategoryAdmin)   