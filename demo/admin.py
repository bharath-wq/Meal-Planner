from django.contrib import admin
from .models import User, Meal, Ingredient, MealIngredient, MealPlan, MealPlanMeal, MealReport



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ['name', 'total_calories', 'created_by']
    list_filter = ['created_by']

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'calories_per_unit', 'unit']

@admin.register(MealIngredient)
class MealIngredientAdmin(admin.ModelAdmin):
    list_display = ['meal', 'ingredient', 'quantity']

@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    list_display = ['user', 'date']
    list_filter = ['user', 'date']

@admin.register(MealPlanMeal)
class MealPlanMealAdmin(admin.ModelAdmin):
    list_display = ['plan', 'meal']

@admin.register(MealReport)
class MealReportAdmin(admin.ModelAdmin):
    readonly_fields = ['avg_calories', 'meal_count']
    list_display = ['start_date', 'end_date', 'avg_calories', 'meal_count']
    ordering = ['-start_date']


