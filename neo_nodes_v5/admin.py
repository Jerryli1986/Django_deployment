from django.contrib import admin

# Register your models here.

from .models import RecordSet,Region,System,Label

admin.site.register(RecordSet)
admin.site.register(Region)
admin.site.register(System)
admin.site.register(Label)
