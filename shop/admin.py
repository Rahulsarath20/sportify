from django.contrib import admin
from .models import *


admin.site.register(category)
admin.site.register(product)

"""
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','image','description')
admin.site.register(category,CategoryAdmin)
admin.site.register(product)
"""