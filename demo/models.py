from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return f"{self.name} ({self.email})"

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    calories_per_unit = models.FloatField()
    unit = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} ({self.unit})"

class Meal(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    total_calories = models.FloatField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class MealIngredient(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField()

    def __str__(self):
        return f"{self.quantity} {self.ingredient.unit} {self.ingredient.name} in {self.meal.name}"

class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"{self.user.name}'s plan on {self.date}"

class MealPlanMeal(models.Model):
    plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.meal.name} in {self.plan.date}'s plan"


class MealReport(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    avg_calories = models.FloatField(null=True, blank=True)
    meal_count = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT ROUND(AVG(meal.total_calories),2), COUNT(DISTINCT meal.id)
                FROM demo_meal AS meal
                JOIN demo_mealplanmeal AS mpm ON mpm.meal_id = meal.id
                JOIN demo_mealplan AS plan ON mpm.plan_id = plan.id
                WHERE plan.date BETWEEN %s AND %s
            """, [self.start_date, self.end_date])
            result = cursor.fetchone()
            self.avg_calories = result[0] or 0
            self.meal_count = result[1] or 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Report: {self.start_date} → {self.end_date}"

