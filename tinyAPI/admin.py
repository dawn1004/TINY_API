from django.contrib import admin
from . models import Question, Calendar, userIntent


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('query', 'answer')


class CalendarAdmin(admin.ModelAdmin):
    list_display = ('date_start', 'date_end', 'remark')


class userIntentAdmin(admin.ModelAdmin):
    list_display = ('intent', 'user')


admin.site.register(Question, QuestionAdmin)
admin.site.register(Calendar, CalendarAdmin)
admin.site.register(userIntent, userIntentAdmin)
