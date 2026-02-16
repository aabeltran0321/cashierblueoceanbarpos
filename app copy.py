from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

main_menu = [
    # Cold Appetizers
    {"kitchen_printer": "Cold Kitchen", "menu_id": 1, "category": "Cold Appetizers", "menu_name": "Wahoo Ceviche", "unit_price": 500, "photo_url": "wahoo_ceviche.jpg"},
    {"kitchen_printer": "Cold Kitchen", "menu_id": 2, "category": "Cold Appetizers", "menu_name": "Tuna Crudo", "unit_price": 500, "photo_url": "tuna_crudo.jpg"},
    {"kitchen_printer": "Cold Kitchen", "menu_id": 3, "category": "Cold Appetizers", "menu_name": "Salmon Poke", "unit_price": 500, "photo_url": "salmon_poke.jpg"},

    # Fresh From The Sea
    {"kitchen_printer": "Cold Kitchen", "menu_id": 4, "category": "Seafood", "menu_name": "Tuna", "unit_price": 400, "photo_url": "tuna_sashimi.jpg"},
    {"kitchen_printer": "Cold Kitchen", "menu_id": 5, "category": "Seafood", "menu_name": "Wahoo", "unit_price": 400, "photo_url": "wahoo_sashimi.jpg"},
    {"kitchen_printer": "Cold Kitchen", "menu_id": 6, "category": "Seafood", "menu_name": "Salmon", "unit_price": 400, "photo_url": "salmon_sashimi.jpg"},

    # Salads and Dips
    {"kitchen_printer": "Cold Kitchen", "menu_id": 7, "category": "Salads and Dips", "menu_name": "Caesar Salad Grande", "unit_price": 600, "photo_url": "caesar_salad.jpg"},
    {"kitchen_printer": "Cold Kitchen", "menu_id": 8, "category": "Salads and Dips", "menu_name": "Nicoise Salad", "unit_price": 550, "photo_url": "nicoise_salad.jpg"},
    {"kitchen_printer": "Cold Kitchen", "menu_id": 9, "category": "Salads and Dips", "menu_name": "Beetroot Hummus", "unit_price": 500, "photo_url": "beetroot_hummus.jpg"},

    # Soup
    {"kitchen_printer": "Hot Kitchen", "menu_id": 10, "category": "Soup", "menu_name": "Fisherman's Pot", "unit_price": 500, "photo_url": "fishermans_pot.jpg"},
    {"kitchen_printer": "Hot Kitchen", "menu_id": 11, "category": "Soup", "menu_name": "Lobster Bisque", "unit_price": 900, "photo_url": "lobster_bisque.jpg"},

    # Crispy Bites
    {"kitchen_printer": "Hot Kitchen", "menu_id": 12, "category": "Crispy Bites", "menu_name": "Calamares", "unit_price": 400, "photo_url": "calamares.jpg"},
    {"kitchen_printer": "Hot Kitchen", "menu_id": 13, "category": "Crispy Bites", "menu_name": "Prawn Croquettes", "unit_price": 400, "photo_url": "prawn_croquettes.jpg"},
    {"kitchen_printer": "Hot Kitchen", "menu_id": 14, "category": "Crispy Bites", "menu_name": "Smoked Buffalo Wings", "unit_price": 400, "photo_url": "buffalo_wings.jpg"},

    # Sandwiches, Burgers and Snacks
    {"kitchen_printer": "Hot Kitchen", "menu_id": 15, "category": "Sandwiches", "menu_name": "Quattro Formaggi Quesadilla", "unit_price": 400, "photo_url": "cheese_quesadilla.jpg"},
    {"kitchen_printer": "Hot Kitchen", "menu_id": 16, "category": "Sandwiches", "menu_name": "Pulled Beef Sandwich", "unit_price": 550, "photo_url": "pulled_beef_sandwich.jpg"},
    {"kitchen_printer": "Hot Kitchen", "menu_id": 17, "category": "Sandwiches", "menu_name": "Surf and Turf Burger", "unit_price": 670, "photo_url": "surf_turf_burger.jpg"},

    # Sizzlers
    {"kitchen_printer": "Hot Kitchen", "menu_id": 18, "category": "Sizzlers", "menu_name": "Mexisisig", "unit_price": 550, "photo_url": "mexisisig.jpg"},
    {"kitchen_printer": "Hot Kitchen", "menu_id": 19, "category": "Sizzlers", "menu_name": "Sizzling Tuna Bites", "unit_price": 450, "photo_url": "sizzling_tuna.jpg"},

    # Pizza
    {"kitchen_printer": "Pizza & Pasta Stn", "menu_id": 20, "category": "Pizza", "menu_name": "Margherita", "unit_price": 600, "photo_url": "margherita_pizza.jpg"},
    {"kitchen_printer": "Pizza & Pasta Stn", "menu_id": 21, "category": "Pizza", "menu_name": "Tropicale", "unit_price": 650, "photo_url": "tropicale_pizza.jpg"},
    {"kitchen_printer": "Pizza & Pasta Stn", "menu_id": 22, "category": "Pizza", "menu_name": "Pepperoni", "unit_price": 700, "photo_url": "pepperoni_pizza.jpg"},
    {"kitchen_printer": "Pizza & Pasta Stn", "menu_id": 23, "category": "Pizza", "menu_name": "Chirashi Sashimi Pizza", "unit_price": 750, "photo_url": "sashimi_pizza.jpg"},

    # Pasta
    {"kitchen_printer": "Pizza & Pasta Stn", "menu_id": 24, "category": "Pasta", "menu_name": "Carbonara Oceanica", "unit_price": 650, "photo_url": "carbonara.jpg"},
    {"kitchen_printer": "Pizza & Pasta Stn", "menu_id": 25, "category": "Pasta", "menu_name": "Ragu Alla Bolognese with Parmesan Espuma", "unit_price": 600, "photo_url": "bolognese.jpg"},
    {"kitchen_printer": "Pizza & Pasta Stn", "menu_id": 26, "category": "Pasta", "menu_name": "Marina Verde Lasagna", "unit_price": 670, "photo_url": "lasagna.jpg"},

    # Mains
    {"kitchen_printer": "Hot Kitchen", "menu_id": 27, "category": "Mains", "menu_name": "Lobster Thermidor", "unit_price": 2400, "photo_url": "lobster_thermidor.jpg"},
    {"kitchen_printer": "Hot Kitchen", "menu_id": 28, "category": "Mains", "menu_name": "Crispy Pork Belly", "unit_price": 600, "photo_url": "crispy_pork_belly.jpg"},
    {"kitchen_printer": "Hot Kitchen", "menu_id": 29, "category": "Mains", "menu_name": "Angus Ribeye", "unit_price": 2500, "photo_url": "angus_ribeye.jpg"},

    # Dessert
    {"kitchen_printer": "Dessert Stn", "menu_id": 30, "category": "Dessert", "menu_name": "Pizza Frita Ala Nutella Smores", "unit_price": 300, "photo_url": "nutella_pizza.jpg"},
    {"kitchen_printer": "Dessert Stn", "menu_id": 31, "category": "Dessert", "menu_name": "Coconut Mousse", "unit_price": 300, "photo_url": "coconut_mousse.jpg"},
    {"kitchen_printer": "Dessert Stn", "menu_id": 32, "category": "Dessert", "menu_name": "Fresh Fruit Platter", "unit_price": 300, "photo_url": "fruit_platter.jpg"},

    # Sides
    {"kitchen_printer": "Hot Kitchen", "menu_id": 33, "category": "Sides", "menu_name": "Rice", "unit_price": 0, "photo_url": "rice.jpg"}, # Price not listed, assumed 0 or custom
    {"kitchen_printer": "Hot Kitchen", "menu_id": 34, "category": "Sides", "menu_name": "Hummus", "unit_price": 0, "photo_url": "hummus_side.jpg"}, # Price not listed
    {"kitchen_printer": "Hot Kitchen", "menu_id": 35, "category": "Sides", "menu_name": "Fries", "unit_price": 0, "photo_url": "fries_side.jpg"}, # Price not listed
    {"kitchen_printer": "Hot Kitchen", "menu_id": 36, "category": "Sides", "menu_name": "Mashed Potato", "unit_price": 0, "photo_url": "mashed_potato_side.jpg"}, # Price not listed
    {"kitchen_printer": "Hot Kitchen", "menu_id": 37, "category": "Sides", "menu_name": "Petite Salad", "unit_price": 0, "photo_url": "petite_salad.jpg"}, # Price not listed
]

# Login
@app.route("/")
def login():
    return render_template("index.html")

# Mainland
@app.route("/mainland/tablemanagement")
def mainland_tablemanagement():
    return render_template("/mainland/tablemanagement.html")

@app.route("/mainland/recreationalactivity")
def mainland_recreationalactivity():
    return render_template("/mainland/recreationalactivity.html")

# Cashier
@app.route("/cashier/tablemanagement")
def cashier_tablemanagement():
    return render_template("/cashier/tablemanagement.html")

@app.route("/cashier/recreationalactivity")
def cashier_recreationalactivity():
    return render_template("/cashier/recreationalactivity.html")

# Waiter
@app.route("/waiter/tablemanagement")
def waiter_tablemanagement():
    return render_template("/waiter/tablemanagement.html")

@app.route("/waiter/recreationactivity")
def waiter_recreational():
    return render_template("/waiter/recreationalactivity.html")

@app.route("/waiter/tablemanagementmenu")
def tablemanagementmenu():
    menu_categories = {}
    for a in main_menu:
        if a['category'] not in menu_categories.keys():
            menu_categories[a['category']] = [a,]
        else:
            menu_categories[a['category']].append(a)
    print(menu_categories)
    return render_template("/waiter/tablemanagementmenu.html", menu_categories=menu_categories)

@app.route("/waiter/recreationalctivitymenu")
def recreationactivitymenu():
    menu_categories = {}
    for a in main_menu:
        if a['category'] not in menu_categories.keys():
            menu_categories[a['category']] = [a,]
        else:
            menu_categories[a['category']].append(a)
    print(menu_categories)
    return render_template("/waiter/recreationalctivitymenu.html", menu_categories=menu_categories)

#API
@app.route('/process_order', methods=['POST'])
def process_order():
    data = request.get_json()
    print("Processing Order:", data)
    return jsonify({"status": "success", "transaction_id": 12345})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)