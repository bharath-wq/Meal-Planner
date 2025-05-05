from django import forms
from .models import Meal, Ingredient, MealIngredient

# Form for creating/editing a Meal
class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['name', 'description']

# Form for linking Ingredients to a Meal
class MealIngredientForm(forms.ModelForm):
    class Meta:
        model = MealIngredient
        fields = ['meal', 'ingredient', 'quantity']

# Optional: A form to create ingredients
class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = '__all__'

'''class MealReportForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()'''
