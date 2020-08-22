from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    # message send
    path('sendMessage/<query>/', views.sendQuery),

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
    path('randoms/<id>/<answer>/', views.updateRandom),


]
# username, password, name, intent
# course_name, college, acronym, campus
