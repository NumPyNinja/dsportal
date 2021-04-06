from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('home', views.homepage, name='home'),
    path('tryEditor', views.tryeditor, name='tryEditor'),
    path('register', views.register, name='register'),
    path('logout', views.logout_request, name='logout'),
    path('login', views.login_request, name='login'),
    path('<slug:course_slug>/', views.course_detail, name='course_detail'),
    path('<slug:course_slug>/<slug:module_slug>/', views.module_detail, name='module_detail'),
    path('<slug:course_slug>/practice', views.practice, name='practice'),
    path('question/<int:q_id>', views.questions, name='question'),

]

