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
]
# username, password, name, intent
# course_name, college, acronym, campus
