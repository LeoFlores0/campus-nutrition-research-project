import pandas as pd

test_data = [
    {"item": "Garden Salad", "description": "Fresh greens with balsamic dressing", "calories": "150", "labels": "Vegan, Gluten-Free"},
    {"item": "Grilled Chicken Breast", "description": "Seasoned chicken with herbs", "calories": "250", "labels": "Gluten-Free"},
    {"item": "Steamed Broccoli", "description": "Lightly steamed fresh broccoli", "calories": "50", "labels": "Vegan, Vegetarian"},
    {"item": "Beef Stir-Fry", "description": "Beef with mixed peppers", "calories": "400", "labels": "None"},
    {"item": "Tofu Scramble", "description": "High protein tofu with spinach", "calories": "200", "labels": "Vegan"},
    {"item": "French Fries", "description": "Deep fried potato strips", "calories": "350", "labels": "Vegetarian"},
    {"item": "Fresh Apple", "description": "Crispy gala apple", "calories": "95", "labels": "Vegan"},
    {"item": "Roasted Turkey", "description": "Slices of roasted turkey", "calories": "180", "labels": "None"}
]

test_df = pd.DataFrame(test_data)
test_df.to_csv('campus_menu.csv', index=False)
print("Test data 'campus_menu.csv' created.")