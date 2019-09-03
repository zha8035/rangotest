from django.contrib import admin

# Register your models here.
from rango.models import Category,Page
from rango.models import UserProfile
class PageAdmin(admin.ModelAdmin):
    list_display=('title','category','url')

#add in this class to customise the admin interface
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('name',)}

admin.site.register(Category,CategoryAdmin)
admin.site.register(Page,PageAdmin)
admin.site.register(UserProfile)
