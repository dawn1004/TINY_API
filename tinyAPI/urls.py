from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    # message send
    path('sendMessage/', views.sendQuery),

    # user crud
    path('createUser/<username>/<password>/<email>/<firstname>/<lastname>/<intent>/', views.createUser),
    path('adminLogin/', views.adminLogin),

    # courses
    path('courses/', views.viewAllCourses),
    path('courses/<college>/', views.getCourseByCollege),
    path('courses/delete/<id>/', views.deleteCourse),
    path('addingcourse/', views.addCourse),

    # endpoints
    path('executives/', views.getExecutives),
    path('executives/edit/', views.updateExecutive),
    path('deans/', views.getDean),
    path('deans/edit/', views.updateDean),
    path('populations/', views.getPopulation),
    path('populations/edit/', views.updatePopulation),
    path('randoms/', views.getRandom),
    path('randoms/<id>/', views.updateRandom),
    path('updateUsername/<oldusername>/<newusername>/<password>/', views.updateUsername),
    path('updatePassword/', views.updatePassword),
    path('actions/', views.getActions),
    path('calendar/', views.getAllCalendar),
    path('calendar/holidays/', views.getAllHolidays),
    path('calendar/addevent/', views.addCalendarEvent),
    path('calendar/updateevent/<id>/', views.updateCalendarEvent),
    path('calendar/<id>/', views.deleteCalendarEvent),
    path('users/', views.getTokenUsers),
    path('usersdata/', views.getUsers),
    path('deleteUser/<id>', views.deleteUser),
    path('chatbotSettings/', views.getChatbotSettings),
    path('updateDisableSetting/', views.updateChatbotSettings),
    path('updateIntroMessage/', views.updateIntroMessage),
    path('tryCaptcha/', views.tryCaptcha),
    path('contacts/', views.getContacts),
    path("updateContact/", views.updateContact),
    path("forgetPassword/", views.forgetPassword),
]
# username, password, name, intent
# course_name, college, acronym, campus
