from django.contrib import admin
from .models import ExtendedUser, Question


# Register your models here.
class ExtendedUserAdmin(admin.ModelAdmin):
    pass


class QuestionsAdmin(admin.ModelAdmin):
    pass


admin.site.register(ExtendedUser, ExtendedUserAdmin)
admin.site.register(Question, QuestionsAdmin)
