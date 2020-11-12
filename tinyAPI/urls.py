from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    # message send
    path('sendMessage/', views.sendQuery),

    # user crud
    path('createUser/<username>/<password>/<email>/<firstname>/<lastname>/<intent>/', views.createUser),
    path('adminLogin/<username>/<password>/', views.adminLogin),

    # courses
    path('courses/', views.viewAllCourses),
    path('courses/<college>/', views.getCourseByCollege),
    path('courses/delete/<id>/', views.deleteCourse),
    path('courses/add/<course_name>/<college>/<acronym>/<campus>/', views.addCourse),

    # endpoints
    path('executives/', views.getExecutives),
    path('executives/<id>/<name>/', views.updateExecutive),
    path('deans/', views.getDean),
    path('deans/<id>/<name>/', views.updateDean),
    path('populations/', views.getPopulation),
    path('populations/<id>/<student_population>/', views.updatePopulation),
    path('randoms/', views.getRandom),
    path('randoms/<id>/', views.updateRandom),
    path('updateUsername/<oldusername>/<newusername>/<password>/', views.updateUsername),
    path('updatePassword/<username>/<password>/<newpassword>/', views.updatePassword),
    path('actions/', views.getActions),
    path('calendar/', views.getAllCalendar),
    path('calendar/holidays/', views.getAllHolidays),
    path('calendar/<event>/<date_start>/<date_end>/<remark>/<name>/<color>/', views.addCalendarEvent),
    path('calendar/<id>/<remark>/', views.updateCalendarEvent),
    path('calendar/<id>/', views.deleteCalendarEvent),
    path('users/', views.getTokenUsers),
    path('usersdata/', views.getUsers)
]
# username, password, name, intent
# course_name, college, acronym, campus
