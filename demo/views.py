from django.shortcuts import render, redirect, get_object_or_404
from .models import Meal, Ingredient, MealIngredient, User, MealPlan, MealPlanMeal
from .forms import MealForm, MealIngredientForm
from django.db import connection
from datetime import date

def meal_list(request):
    meals = Meal.objects.all()
    return render(request, 'demo/meal_list.html', {'meals': meals})

def create_meal(request):
    if request.method == 'POST':
        form = MealForm(request.POST)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.created_by = User.objects.first()
            meal = form.save()
            return redirect('edit_meal', meal.id)
    else:
        form = MealForm()
    return render(request, 'demo/create_meal.html', {'form': form})

def edit_meal(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id)
    ingredients = MealIngredient.objects.filter(meal=meal)
    return render(request, 'demo/edit_meal.html', {
        'meal': meal,
        'ingredients': ingredients
    })

def add_ingredient_to_meal(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id)

    if request.method == 'POST':
        form = MealIngredientForm(request.POST)
        if form.is_valid():
            meal_ingredient = form.save()
            return redirect('edit_meal', meal_id=meal.id)
    else:
        form = MealIngredientForm(initial={'meal': meal})

    return render(request, 'demo/add_ingredient.html', {
        'form': form,
        'meal': meal
    })

def delete_meal(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id)
    if request.method == 'POST':
        meal.delete()
        return redirect('meal_list')
    return render(request, 'demo/confirm_delete_meal.html', {'meal': meal})

def delete_meal_ingredient(request, ingredient_id):
    meal_ingredient = get_object_or_404(MealIngredient, id=ingredient_id)
    meal_id = meal_ingredient.meal.id
    if request.method == 'POST':
        meal_ingredient.delete()
        return redirect('edit_meal', meal_id=meal_id)
    return render(request, 'demo/confirm_delete_ingredient.html', {
        'ingredient': meal_ingredient
    })

def meal_calorie_report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    selected_user = request.GET.get('user')
    selected_meal = request.GET.get('meal')
    min_calories = request.GET.get('min_calories')
    max_calories = request.GET.get('max_calories')

    avg_calories = None
    meal_count = 0
    avg_ingredients = None
    most_used_ingredient = None
    ingredient_freq = 0

    users = User.objects.all()
    meals = Meal.objects.all()

    filters = []
    params = []

    if start_date and end_date:
        filters.append("plan.date BETWEEN %s AND %s")
        params += [start_date, end_date]

    if selected_user:
        filters.append("plan.user_id = %s")
        params.append(selected_user)

    if selected_meal:
        filters.append("meal.id = %s")
        params.append(selected_meal)

    if min_calories and max_calories:
        filters.append("meal.total_calories BETWEEN %s AND %s")
        params += [min_calories, max_calories]

    where_clause = " AND ".join(filters) if filters else "1=1"

    if filters:
        with connection.cursor() as cursor:
            # 1. Average calories and meal count
            cursor.execute(f"""
                SELECT 
                    AVG(meal.total_calories) AS avg_calories,
                    COUNT(DISTINCT meal.id) AS meal_count
                FROM demo_meal AS meal
                JOIN demo_mealplanmeal AS mpm ON mpm.meal_id = meal.id
                JOIN demo_mealplan AS plan ON mpm.plan_id = plan.id
                WHERE {where_clause}
            """, params)
            result = cursor.fetchone()
            avg_calories = result[0]
            meal_count = result[1]

            # 2. Average ingredients per meal
            cursor.execute(f"""
                SELECT AVG(ingredient_count) FROM (
                    SELECT COUNT(DISTINCT mi.ingredient_id) AS ingredient_count
                    FROM demo_meal AS meal
                    JOIN demo_mealplanmeal AS mpm ON mpm.meal_id = meal.id
                    JOIN demo_mealplan AS plan ON mpm.plan_id = plan.id
                    JOIN demo_mealingredient AS mi ON mi.meal_id = meal.id
                    WHERE {where_clause}
                    GROUP BY meal.id
                ) sub;
            """, params)
            avg_ingredients = cursor.fetchone()[0]

            # 3. Most frequently used ingredient
            cursor.execute(f"""
                SELECT i.name, COUNT(*) as freq
                FROM demo_meal AS meal
                JOIN demo_mealplanmeal AS mpm ON mpm.meal_id = meal.id
                JOIN demo_mealplan AS plan ON mpm.plan_id = plan.id
                JOIN demo_mealingredient AS mi ON mi.meal_id = meal.id
                JOIN demo_ingredient AS i ON i.id = mi.ingredient_id
                WHERE {where_clause}
                GROUP BY i.name
                ORDER BY freq DESC
                LIMIT 1;
            """, params)
            row = cursor.fetchone()
            if row:
                most_used_ingredient, ingredient_freq = row

    return render(request, 'demo/meal_report.html', {
        'avg_calories': avg_calories,
        'meal_count': meal_count,
        'avg_ingredients': avg_ingredients,
        'most_used_ingredient': most_used_ingredient,
        'ingredient_freq': ingredient_freq,
        'start_date': start_date,
        'end_date': end_date,
        'min_calories': min_calories,
        'max_calories': max_calories,
        'users': users,
        'meals': meals,
        'selected_user': selected_user,
        'selected_meal': selected_meal,
    })