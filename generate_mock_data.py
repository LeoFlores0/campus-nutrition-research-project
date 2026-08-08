import pandas as pd
import numpy as np

# Set seed for random number generator reproducibility
np.random.seed(42)

# Define pool of menu items and their dietary labels
menu_pool = [
    {"item_name": "Scrambled Eggs", "dietary_label": "Vegetarian"},
    {"item_name": "Garden Salad", "dietary_label": "Vegan, Gluten-Free"},
    {"item_name": "Grilled Chicken Breast", "dietary_label": "Gluten-Free"},
    {"item_name": "Steamed Broccoli", "dietary_label": "Vegan, Vegetarian, Gluten-Free"},
    {"item_name": "French Fries", "dietary_label": "Vegetarian, Gluten-Free"},
    {"item_name": "Mac and Cheese", "dietary_label": "Vegetarian"},
    {"item_name": "Beef Stir-Fry", "dietary_label": ""},
    {"item_name": "Tofu Scramble", "dietary_label": "Vegan, Vegetarian"}
]

# Randomly sample 60 items from the menu pool with replacement
n_records = 60
selected_items = np.random.choice(menu_pool, n_records)

data = []
# Iterate through selected items to construct mock nutritional records
for entry in selected_items:
    # Generate overall calorie count
    calories = np.random.randint(80, 650)
    
    # Adjust specific nutrient ranges based on dietary label classification
    if "Vegan" in entry["dietary_label"] or "Vegetarian" in entry["dietary_label"]:
        protein = np.random.randint(3, 15)       
        sat_fat = np.random.randint(0, 5)
        fiber = np.random.randint(2, 8)        
    else:
        protein = np.random.randint(15, 38)      
        sat_fat = np.random.randint(3, 14)       
        fiber = np.random.randint(0, 3)

    # Compile item metadata and randomized nutrient profiles into a row
    row = {
        "item_name": entry["item_name"],
        "dietary_label": entry["dietary_label"],
        "calories": calories,
        "protein_g": protein,
        "carbs_g": np.random.randint(5, 55),
        "fat_g": np.random.randint(1, 25),
        "saturated_fat_g": sat_fat,
        "sodium_mg": np.random.randint(150, 1100), 
        "fiber_g": fiber,
        "added_sugars_g": np.random.randint(0, 14)
    }
    data.append(row)

# Convert compiled records to a pandas DataFrame and write to a CSV file
df = pd.DataFrame(data)
df.to_csv('campus_menu_mock.csv', index=False)
print("Success")