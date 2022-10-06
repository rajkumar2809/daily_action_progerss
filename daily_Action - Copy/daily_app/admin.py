from asyncio import Task
from django.contrib import admin
from daily_app.models import *

# Register your models here.


class NewUserAdmin(admin.ModelAdmin):
    model= NewUser
    list_display = ['id',"user_name","first_name"]


class EgroupAdmin(admin.ModelAdmin):
    model= Egroup
    list_display = ['id',"name","lead_id"]

class ProjectAdmin(admin.ModelAdmin):
    model= Project
    list_display = ['id',"name",]

class TaskAdmin(admin.ModelAdmin):
    model= Tasks
    list_display = ['id',"project_id","description"]

admin.site.register(NewUser , NewUserAdmin)
admin.site.register(Egroup , EgroupAdmin)
admin.site.register(Project , ProjectAdmin)
admin.site.register(Tasks , TaskAdmin)

admin.site.register(ChatMessage)