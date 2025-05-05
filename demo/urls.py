from django.urls import path

from . import views

urlpatterns = [
    path('meals/create/', views.create_meal, name='create_meal'),
    path('meals/<int:meal_id>/edit/', views.edit_meal, name='edit_meal'),
    path('meals/<int:meal_id>/delete/', views.delete_meal, name='delete_meal'),
    path('meals/<int:meal_id>/add-ingredient/', views.add_ingredient_to_meal, name='add_ingredient_to_meal'),
    path('ingredients/<int:ingredient_id>/delete/', views.delete_meal_ingredient, name='delete_meal_ingredient'),
    path('meals/', views.meal_list, name='meal_list'),
    path('report/', views.meal_calorie_report, name='meal_calorie_report'),
]