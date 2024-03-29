from django.contrib import admin
from . models import Question, Calendar, userIntent, Course, Executive, Dean, Population, Random, Action, ChatbotSettings, Contact, BetaTest


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


class ChatbotSettingsAdmin(admin.ModelAdmin):
    list_display = ('key', 'message', 'is_disable')

class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "office_name", "email", "facebook", "landline", "college_secretary", "ref")


class BetaTestAdmin(admin.ModelAdmin):
    list_display = ('message', 'accuracy')

admin.site.register(Question, QuestionAdmin)
admin.site.register(Calendar, CalendarAdmin)
admin.site.register(userIntent, userIntentAdmin)
admin.site.register(Course, CourseAdmin)

admin.site.register(Executive, ExecutiveAdmin)
admin.site.register(Dean, DeanAdmin)
admin.site.register(Population, PopulationAdmin)
admin.site.register(Random, RandomAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(ChatbotSettings, ChatbotSettingsAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(BetaTest, BetaTestAdmin)
