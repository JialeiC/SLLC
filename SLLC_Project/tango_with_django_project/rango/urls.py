from django.urls import path
from rango import views

app_name = 'rango'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
    path('add_category/', views.add_category, name='add_category'),
    path('category/<slug:category_name_slug>/add_page/', views.add_page, name='add_page'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('restricted/', views.restricted, name='restricted'),
    path('logout/', views.user_logout, name='logout'),
    path('homepage/', views.homepage, name='homepage'),
    path('questions/', views.questions, name='questions'),
    path('questions/<int:question_id>', views.showComment, name='questions'),
    path('add_question/', views.add_question, name='add_question'),
    path('search_do/', views.search_do, name="search"),
    path('addquestion_do/', views.addquestion_do, name="addquestion_do"),
    path('questions/', views.add_comment, name='add_comment'),
]