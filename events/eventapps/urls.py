from django.urls import path
from . import views

urlpatterns=[
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('editProfile/',views.editProfile,name='editProfile'),
    path('editEvent/<int:uid>/',views.editEvent,name='editEvent'),
    path('createEvent/',views.createEvent,name='createEvent'),
    path('deleteEvent/<int:did>/',views.deleteEvent,name='deleteEvent'),
    path('viewMyEvents/',views.viewMyEvents,name='viewMyEvents'),
    path('viewAllEvents/',views.viewAllEvents,name='viewAllEvents'),
    path('viewProfile/',views.viewProfile,name='viewProfile')

]