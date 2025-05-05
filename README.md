Meal Planner Django Application
This project is a Meal Planning and Nutrition Tracker web application built with Django. Users can create meals, associate ingredients with calorie values, and assign meals to personalized meal plans. The application includes basic CRUD functionality, data reporting using both Django ORM and raw SQL queries (prepared statements), and admin views for management.

🚀 Features
Add, edit, and delete meals
Associate ingredients with meals (and specify quantity)
Track total calories for each meal
Create meal plans by date and assign meals
View dynamic reports (average calories, most used ingredient, etc.)
Admin interface for easy content management
Uses both Django ORM and prepared SQL statements for data access

🗃️ Database Schema Overview
Core Models:
User: Tracks user who created meals or plans
Ingredient: Ingredient name, calories per unit, and unit type
Meal: Combines ingredients, records total calories
MealIngredient: Many-to-many relationship between meals and ingredients with quantity
MealPlan: Assigned to a user and a specific date
MealPlanMeal: Connects meals to a meal plan

📈 Reports (Prepared Statement Queries)
Average calories over time period
Meal count per date range
Average ingredients per meal
Most frequently used ingredient
Accessible from /demo/meal_report/

🔐 Admin Interface
Visit /admin/
Add and edit meals, ingredients, users, and plans
View and filter content by fields like date, user, or meal name

📌 Setup Instructions
Clone the repository:
git clone <your-repo-url>
cd cs348project
Install dependencies:
pip install -r requirements.txt
Apply migrations:
python manage.py makemigrations
python manage.py migrate
Create admin user:
python manage.py createsuperuser
Start development server:
python manage.py runserver
Access the app:
User interface: http://127.0.0.1:8000/demo/
Admin interface: http://127.0.0.1:8000/admin/

📄 Indexes Used
Auto-generated indexes for all primary and foreign keys
Suggested manual indexes:
Meal.total_calories (for range filters in reports)
MealPlan.date (for filtering by date)
Ingredient.name (if used in search/autocomplete)
See Index Documentation for detailed explanations.

✍️ Author
Bharath Sadagopan

📝 License
This project is for academic purposes under Purdue University's CS348 course. Not intended for production use.

💬 Questions?
Please reach out via the course portal or contact the project author.

