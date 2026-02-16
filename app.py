from flask import Flask, request, render_template, jsonify

app = Flask(__name__)


main_menu = [
    {"kitchen_printer": "Kitchen A", "menu_id": 1, "category": "Main Dish", "menu_name": "Chicken Adobo", "unit_price": 199, "photo_url": "chicken_adobo.jpg"},
    {"kitchen_printer": "Kitchen A", "menu_id": 2, "category": "Main Dish", "menu_name": "Pork Sinigang", "unit_price": 229, "photo_url": "pork_sinigang.avif"},
    {"kitchen_printer": "Kitchen A", "menu_id": 3, "category": "Main Dish", "menu_name": "Beef Tapa", "unit_price": 189, "photo_url": "beef_tapa.jpg"},
    {"kitchen_printer": "Kitchen A", "menu_id": 4, "category": "Main Dish", "menu_name": "Grilled Pork Chop", "unit_price": 249, "photo_url": "pork_chop.jpeg"},

    {"kitchen_printer": "Kitchen B", "menu_id": 5, "category": "Side Dish", "menu_name": "Garlic Rice", "unit_price": 49, "photo_url": "garlic_rice.jpg"},
    {"kitchen_printer": "Kitchen B", "menu_id": 6, "category": "Side Dish", "menu_name": "Steamed Vegetables", "unit_price": 79, "photo_url": "steam_vegetables.jpg"},
    {"kitchen_printer": "Kitchen B", "menu_id": 7, "category": "Side Dish", "menu_name": "French Fries", "unit_price": 99, "photo_url": "french_fries.jpg"},
    {"kitchen_printer": "Kitchen B", "menu_id": 8, "category": "Side Dish", "menu_name": "Mashed Potato", "unit_price": 89, "photo_url": "mashed_potatoes.jpg"},

    {"kitchen_printer": "Kitchen C", "menu_id": 9, "category": "Beverage", "menu_name": "Iced Tea", "unit_price": 149, "photo_url": "iced_tea.jpg"},
    {"kitchen_printer": "Kitchen C", "menu_id": 10, "category": "Beverage", "menu_name": "Mango Shake", "unit_price": 99, "photo_url": ""},
    {"kitchen_printer": "Kitchen C", "menu_id": 11, "category": "Beverage", "menu_name": "San Mig Light", "unit_price": 169, "photo_url": "beer.jpg"},
    {"kitchen_printer": "Kitchen C", "menu_id": 12, "category": "Beverage", "menu_name": "Coke", "unit_price": 79, "photo_url": "coke.jpg"},

    {"kitchen_printer": "Kitchen D", "menu_id": 13, "category": "Dessert", "menu_name": "Halo-Halo", "unit_price": 129, "photo_url": "halo_halo.jpg"},
    {"kitchen_printer": "Kitchen D", "menu_id": 14, "category": "Dessert", "menu_name": "Leche Flan", "unit_price": 89, "photo_url": "leche_plan.jpg"},
    {"kitchen_printer": "Kitchen D", "menu_id": 15, "category": "Dessert", "menu_name": "Chocolate Cake", "unit_price": 149, "photo_url": "chocolate_cake.jpg"},
    {"kitchen_printer": "Kitchen D", "menu_id": 16, "category": "Dessert", "menu_name": "Ice Cream", "unit_price": 99, "photo_url": "ice_cream.webp"},
]

# FULL_MENU = {
#     "Main Dish": [
#         {"id": 101, "menu_name": "Chicken Adobo", "unit_price": 199, "photo_url": "chicken_adobo.jpg"},
#         {"id": 102, "menu_name": "Pork Sinigang", "unit_price": 229, "photo_url": "pork_sinigang.avif"},
#         {"id": 103, "menu_name": "Beef Tapa", "unit_price": 189, "photo_url": "beef_tapa.jpg"},
#         {"id": 104, "menu_name": "Grilled Pork Chop", "unit_price": 249, "photo_url": "pork_chop.jpeg"},
#     ],
#     "Side Dish": [
#         {"id": 201, "menu_name": "Garlic Rice", "unit_price": 49, "photo_url": "garlic_rice.jpg"},
#         {"id": 202, "menu_name": "Steamed Vegetables", "unit_price": 79, "photo_url": "steam_vegetables.jpg"},
#         {"id": 203, "menu_name": "French Fries", "unit_price": 99, "photo_url": "french_fries.jpg"},
#         {"id": 204, "menu_name": "Mashed Potato", "unit_price": 89, "photo_url": "mashed_potatoes.jpg"},
#     ],
#     "Beverage": [
#         {"id": 301, "menu_name": "Iced Tea", "unit_price": 149, "photo_url": "iced_tea.jpg"},
#         {"id": 302, "menu_name": "Mango Shake", "unit_price": 99, "photo_url": "mango_shake.jpg"},
#         {"id": 303, "menu_name": "San Mig Light", "unit_price": 169, "photo_url": "beer.jpg"},
#         {"id": 304, "menu_name": "Coke", "unit_price": 79, "photo_url": "coke.jpg"},
#     ],
#     "Dessert": [
#         {"id": 401, "menu_name": "Halo-Halo", "unit_price": 129, "photo_url": "halo_halo.jpg"},
#         {"id": 402, "menu_name": "Leche Flan", "unit_price": 89, "photo_url": "leche_plan.jpg"},
#         {"id": 403, "menu_name": "Chocolate Cake", "unit_price": 149, "photo_url": "chocolate_cake.jpg"},
#         {"id": 404, "menu_name": "Ice Cream", "unit_price": 99, "photo_url": "ice_cream.webp"},
#     ]
# }

@app.route("/")
def login():
    return render_template("index.html")

@app.route("/tablemanagement")
def tablemanagement():
    return render_template("tablemanagement.html")

@app.route("/menu")
def menu():
    menu_categories = {}
    for a in main_menu:
        if a['category'] not in menu_categories.keys():
            menu_categories[a['category']] = [a,]
        else:
            menu_categories[a['category']].append(a)
    print(menu_categories)
    return render_template("menu.html", menu_categories=menu_categories)

@app.route('/process_order', methods=['POST'])
def process_order():
    data = request.get_json()
    print("Processing Order:", data)
    return jsonify({"status": "success", "transaction_id": 12345})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)