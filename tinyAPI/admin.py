from django.contrib import admin
from . models import Question, Calendar, userIntent, Course, Executive, Dean, Population, Random, Action


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('query', 'answer')


class CalendarAdmin(admin.ModelAdmin):
    list_display = ('date_start', 'date_end', 'event', 'remark', 'name', 'color')


class userIntentAdmin(admin.ModelAdmin):
    list_display = ('intent', 'user')


class CourseAdmin(admin.ModelAdmin):
    list_display = ('course', 'college', 'college_acronym', 'campus')


class ExecutiveAdmin(admin.ModelAdmin):
    list_display = ('position', 'name')


class DeanAdmin(admin.ModelAdmin):
    list_display = ('college', 'name')


class PopulationAdmin(admin.ModelAdmin):
    list_display = ('college', 'student_population')


class RandomAdmin(admin.ModelAdmin):
    list_display = ('key', 'answer', 'question')

class ActionAdmin(admin.ModelAdmin):
    list_display = ('action', 'date', 'time')


admin.site.register(Question, QuestionAdmin)
admin.site.register(Calendar, CalendarAdmin)
admin.site.register(userIntent, userIntentAdmin)
admin.site.register(Course, CourseAdmin)

admin.site.register(Executive, ExecutiveAdmin)
admin.site.register(Dean, DeanAdmin)
admin.site.register(Population, PopulationAdmin)
admin.site.register(Random, RandomAdmin)
admin.site.register(Action, ActionAdmin)
