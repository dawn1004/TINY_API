from django.contrib import admin
from . models import Question, Calendar


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('query', 'answer')


class CalendarAdmin(admin.ModelAdmin):
    list_display = ('date_start', 'date_end', 'remark')


admin.site.register(Question, QuestionAdmin)
admin.site.register(Calendar, CalendarAdmin)
