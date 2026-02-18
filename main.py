import db_connector
from db_connector import get_connection
from flask import Flask, request, render_template, jsonify, session, url_for, redirect
import json
import os
from flask_cors import CORS
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from werkzeug.utils import secure_filename
from db_models.login_model import employee_login
from db_models.employee_model import get_employee, post_employee, put_employee, delete_employee
from db_models.main_menu_model import get_main_menu,  get_main_menu_category, post_main_menu, put_main_menu, delete_main_menu
from db_models.table_management_model import get_table, post_table, put_table, delete_table
from db_models.transactions_model import get_transaction, get_transaction_by_transaction_id, post_transaction, put_transaction,delete_transaction
from db_models.recreational_activities_model import get_recreational_activity, post_recreational_activity, put_recreational_activity, delete_recreational_activity
from db_models.decks_model import get_deck, post_deck, put_deck, delete_deck
from db_models.orders_model import get_order, post_order, put_order, delete_order
from db_models.table_guest_model import get_table_guest
from db_models.login_model import employee_login
from db_models.employee_model import get_employee, post_employee, put_employee, delete_employee
from db_models.main_menu_model import get_main_menu,  get_main_menu_category, post_main_menu, put_main_menu, delete_main_menu
from db_models.table_management_model import get_table, post_table, put_table, delete_table
from db_models.transactions_model import get_transaction, get_pending_transactions, get_transaction_by_transaction_id, post_transaction, put_transaction,delete_transaction
from db_models.recreational_activities_model import get_recreational_activity, get_recreational_activities_with_transaction, post_recreational_activity, put_recreational_activity, put_recreational_activity_transaction_status, delete_recreational_activity
from db_models.decks_model import get_deck, post_deck, put_deck, delete_deck
from db_models.orders_model import get_order, post_order, put_order, delete_order
from db_models.table_guest_model import get_table_guest, get_all_table_guest
app = Flask(__name__)
CORS(app)


template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "palawan_front", "templates")
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "palawan_front", "static")

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.secret_key = "palawan@2026!"

MAIN_MENU_FOLDER = Path('Menu_Image')
MAIN_MENU_FOLDER.mkdir(parents = True, exist_ok = True)


RECREATIONAL_FOLDER = Path('Recereational_Image')
RECREATIONAL_FOLDER.mkdir(parents = True, exist_ok = True)

app.secret_key = "supersecretkey"

# ---------------------------------
#             LOGIN
# ---------------------------------
# Just render the login page
# @app.route("/")
# def index():
#     return render_template("index.html")

# Only handle login POST
@app.route("/login", methods=["POST"])
def login_route():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()

    employee_id = data.get("employee_id")
    password = data.get("password")

    if not employee_id or not password:
        return jsonify({"success": False, "message": "employee_id and password required"}), 400

    user = login(employee_id, password)

    if user:
        session["employee_id"] = user['employee_id']
        session["position"] = user.get("position", "staff").capitalize()
        session["name"] = f"{user.get('firstName')} {user.get('lastName')}"

        return jsonify({
            "success": True,
            "message": "Login successful",
            "position": session["position"],
            "name": session["name"]
        })

    return jsonify({"success": False, "message": "Invalid employee_id or password"}), 401

# --------------------------------
#           TABLEGUEST
# -------------------------------
@app.route("/table_guest/<int:tableID>")
def get_table_guest_route(tableID):
    try:
        result = get_table_guest(tableID=tableID)
        if tableID and not result:
            return jsonify({
                "status": "error",
                "message": "Employee not found"
            }), 404

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# ---------------------------------
#             EMPLOYEE
# ---------------------------------


@app.route("/employeemanagement")
def staffmanagement():
    # if 'role' not in session or session['role'] !='Manager':
    #     return redirect(url_for('index'))
    return render_template("staff.html")

@app.route("/employees")
@app.route("/employees/<int:id>")
def get_employee_route(id=None):
    # if 'role' not in session:
    #     return redirect(url_for('index'))

    try:
        result = get_employee(id=id)

        if id and not result:
            return jsonify({
                "status": "error",
                "message": "Employee not found"
            }), 404

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/employees", methods=["POST"])
def post_employee_route():
    # if 'role' not in session:
    #      return redirect(url_for('index'))

    try:
        employee_data = request.get_json()

        if not employee_data:
            return jsonify({
                "status": "error",
                "message": "No input data provided"
            }), 400

        result = post_employee(employee_data=employee_data)

        if result['status'] == "success":
            return jsonify(result), 201
        else:
            return jsonify(result), 500

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    
@app.route("/employees/<int:id>", methods=["PUT"])
def put_employee_route(id):
    # if 'role' not in session:
    #     return redirect(url_for('index'))

    try:
        employee_data = request.get_json()

        if not employee_data:
            return jsonify({
                "status": "error",
                "message": "No input data provided"
            }), 400

        result = put_employee(id=id, employee_data=employee_data)

        return jsonify(result)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/employees/<int:id>", methods=["DELETE"])
def delete_employee_route(id):
    # if 'role' not in session:
    #     return redirect(url_for('index'))

    try:
        result = delete_employee(id=id)

        if result['deleted_rows'] == 0:
            return jsonify({
                "status": "error",
                "message": "Employee Not Found"
            }), 404

        return jsonify(result)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# ---------------------------------
#             MENU
# ---------------------------------

@app.route("/main_menu")
@app.route("/main_menu/<int:menu_id>")
def get_menu_route(menu_id=None):
    result = get_main_menu(menu_id=menu_id)

    if menu_id and not result:
        return jsonify({"status": "error", "message": "Menu item not found"}), 404

    return jsonify(result), 200
@app.route("/main_menu/<string:category>")
def get_menu_category_route(category):
    result = get_main_menu_category(category=category)

    if category and not result:
        return jsonify({"status": "error", "message": "category not found"}), 404
    
    return jsonify(result), 200

@app.route("/main_menu", methods=["POST"])
def post_menu_route():
    try:
        data = request.form.to_dict()

        # Handle picture upload
        if "picture" in request.files:
            file = request.files["picture"]
            if file.filename != "":
                filename = secure_filename(file.filename)
                filepath = str(MAIN_MENU_FOLDER / filename)
                file.save(filepath)
                data["picture_url"] = filepath
            else:
                data["picture_url"] = None
        else:
            data["picture_url"] = None

        result = post_main_menu(data)
        return jsonify(result), 201 if result["status"] == "success" else 500

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route("/main_menu/<int:menu_id>", methods=["PUT"])
def put_menu_route(menu_id):
    try:
        data = request.form.to_dict()

        # Handle picture upload
        if "picture" in request.files:
            file = request.files["picture"]
            if file.filename != "":
                filename = secure_filename(file.filename)
                filepath = str(MAIN_MENU_FOLDER / filename)
                file.save(filepath)
                data["picture_url"] = filepath

        result = put_main_menu(menu_id, data)
        return jsonify(result)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route("/main_menu/<int:menu_id>", methods=["DELETE"])
def delete_menu_route(menu_id):
    try:
        result = delete_main_menu(menu_id)
        if result["deleted_rows"] == 0:
            return jsonify({"status": "error", "message": "Menu item not found"}), 404
        return jsonify(result)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
    
# ---------------------------------
#               Table
# ---------------------------------

@app.route("/tables")
@app.route("/tables/<int:tableID>")
def get_table_route(tableID=None):
    try:
        result = get_table(tableID=tableID)

        if tableID and not result:
            return jsonify({
                "status": "error",
                "message": "Table not found"
            }), 404

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route("/tables", methods=["POST"])
def post_table_route():
    try:
        table_data = request.get_json()

        if not table_data:
            return jsonify({
                "status": "error",
                "message": "No input data provided"
            }), 400

        result = post_table(table_data=table_data)

        if result["status"] == "success":
            return jsonify(result), 201
        else:
            return jsonify(result), 500

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/tables/<int:tableID>", methods=["PUT"])
def put_table_route(tableID):
    try:
        table_data = request.get_json()

        if not table_data:
            return jsonify({
                "status": "error",
                "message": "No input data provided"
            }), 400

        result = put_table(tableID=tableID, table_data=table_data)

        return jsonify(result)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/tables/<int:tableID>", methods=["DELETE"])
def delete_table_route(tableID):
    try:
        result = delete_table(tableID=tableID)

        if result["deleted_rows"] == 0:
            return jsonify({
                "status": "error",
                "message": "Table not found"
            }), 404

        return jsonify(result)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    
# ---------------------------------
#               Transactions
# ---------------------------------

@app.route("/transactions")
@app.route("/transactions/<int:id>")
def get_transaction_route(id=None):
    try:
        result = get_transaction(id=id)

        if id and not result:
            return jsonify({
                "status": "error",
                "message": "Transaction not found"
            }), 404

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
   
@app.route("/transactions/transaction_id/<string:transaction_id>")
def get_transaction_by_receipt_route(transaction_id=None):
    try:
        if not transaction_id:
            return jsonify({
                "status": "error",
                "message": "transaction_id is required"
            }), 400

        result = get_transaction_by_transaction_id(transaction_id)

        if not result:
            return jsonify({
                "status": "error",
                "message": "Transaction not found"
            }), 404

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route("/transactions", methods=["POST"])
def post_transaction_route():

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "status": "error",
                "message": "No input data provided"
            }), 400

        result = post_transaction(data=data)
        print(result)

        if result["status"] == "success":
            return jsonify(result), 201
        else:
            return jsonify(result), 500

    except Exception as e:
        print(e)
        return jsonify({"status": "error", "message": str(e)})

@app.route("/transactions/<int:id>", methods=["PUT"])
def put_transaction_route(id):
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "status": "error",
                "message": "No input data provided"
            }), 400

        result = put_transaction(id=id, data=data)

        return jsonify(result)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# @app.route("/transactions/amount_paid/<int:id>", methods = ["PUT"])
# def put_transaction_amount_paid_route(id):
#     try:
#         data = request.get_json()
#         if not data:
#             return jsonify({
#                 "status": "error",
#                 "message": "No input data provided"
#             }), 400
#         result = put_amount_paid(id = id, data=data)

#         return jsonify(result)
#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)})

@app.route("/transactions/<int:id>", methods=["DELETE"])
def delete_transaction_route(id):
    try:
        result = delete_transaction(id=id)

        if result["deleted_rows"] == 0:
            return jsonify({
                "status": "error",
                "message": "Transaction not found"
            }), 404

        return jsonify(result)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    


# ---------------------------------
#               Recreational_activities
# ---------------------------------


@app.route("/recreational_activities")
@app.route("/recreational_activities/<int:activity_id>")
def get_recreational_activity_route(activity_id=None):
    result = get_recreational_activity(activity_id=activity_id)

    if activity_id and not result:
        return jsonify({"status": "error", "message": "Activity not found"}), 404

    return jsonify(result), 200


@app.route("/recreational_activities", methods=["POST"])
def post_recreational_activity_route():
    try:
        data = request.form.to_dict()

        # Handle picture upload
        if "picture" in request.files:
            file = request.files["picture"]
            if file.filename != "":
                filename = secure_filename(file.filename)
                filepath = str(RECREATIONAL_FOLDER / filename)
                file.save(filepath)
                data["picture_url"] = filepath
            else:
                data["picture_url"] = None
        else:
            data["picture_url"] = None

        result = post_recreational_activity(data)

        return jsonify(result), 201 if result["status"] == "success" else 500

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/recreational_activities/<int:activity_id>", methods=["PUT"])
def put_recreational_activity_route(activity_id):
    try:
        data = request.form.to_dict()

        # Handle picture upload
        if "picture" in request.files:
            file = request.files["picture"]
            if file.filename != "":
                filename = secure_filename(file.filename)
                filepath = str(RECREATIONAL_FOLDER / filename)
                file.save(filepath)
                data["picture_url"] = filepath

        result = put_recreational_activity(activity_id, data)
        return jsonify(result)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/recreational_activities/<int:activity_id>", methods=["DELETE"])
def delete_recreational_activity_route(activity_id):
    try:
        result = delete_recreational_activity(activity_id)

        if result["deleted_rows"] == 0:
            return jsonify({"status": "error", "message": "Activity not found"}), 404

        return jsonify(result)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
# ---------------------------------
#             DECK
# ---------------------------------

@app.route("/deck")
@app.route("/deck/<int:id>")
def get_deck_route(id = None):
    result = get_deck(id=id)

    if id and not result:
        return jsonify({"status": "error", "message": "Activity not found"}), 404

    return jsonify(result), 200



@app.route("/deck", methods=["POST"])
def post_deck_route():
    try:
        deck_data = request.get_json()

        if not deck_data:
            return jsonify({
                "status": "error",
                "message": "No input data provided"
            }), 400
        
        result = post_deck(deck_data=deck_data)

        if result['status'] == 'success':
            return jsonify(result), 201
        else:
            return jsonify(result),500

    except Exception as e:
          return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/deck/<int:id>", methods = ["PUT"])
def put_deck_route(id):
    try:
        deck_data = request.get_json()
        if not deck_data:
            return jsonify({
                "status": "error",
                "message": "No input data provided"
            }), 400
        result = put_deck(id=id, deck_data=deck_data)

        return jsonify(result)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/deck/<int:id>", methods = ["DELETE"])
def delete_deck_route(id):
    try:
        result = delete_deck(id=id)


        if result['deleted_rows'] == 0:
            return jsonify({
                "status": "error",
                "message": "Deck Not Found"
            }), 404

        return jsonify(result)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
# --------------------------------
#             ORDERS
# --------------------------------
@app.route("/orders")
@app.route("/orders/<int:order_id>")
def get_orders_routes(order_id=None):
    try:
        result = get_order(order_id=order_id)

        if order_id and not result:
            return jsonify({
                "status": "error",
                "message": "order not found"
            }), 404

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/orders", methods=["POST"])
def post_order_route():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "status": "error",
                "message": "No input data provided"
            }), 400

        result = post_order(order_data=data)

        if result["status"] == "success":
            return jsonify(result), 201
        else:
            return jsonify(result), 500

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})



@app.route("/orders/<int:order_id>", methods=["PUT"])
def put_order_route(order_id):
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "status": "error",
                "message": "No input data provided"
            }), 400

        result = put_order(order_id=order_id, order_data=data)

        return jsonify(result)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})



@app.route("/orders/<int:order_id>", methods=["DELETE"])
def delete_order_route(order_id):
    try:
        result = delete_order(order_id=order_id)

        if result["deleted_rows"] == 0:
            return jsonify({
                "status": "error",
                "message": "Order not found"
            }), 404

        return jsonify(result)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
# --------------------------------
#         Arjun
# -------------------------------


@app.route("/dashboard_manager")
def dashboard_manager():

    all_transaction = get_transaction()
   
    return render_template("dashboard_manager.html", all_transaction=all_transaction)

@app.route("/dashboard/form/<int:id>")
def dashboard_form(id):
    print("Transaction ID:", id)
    txn = get_transaction(id=id)
    print("Transaction:", txn)
    if not txn:
        return "Transaction not found", 404
    return render_template("dashboard-form-view.html", transaction=txn)

@app.route("/", methods = ["GET","POST"])
def login():

    if request.method == "POST":
        employee_id = request.form.get("employee_id")
        password = request.form.get("password")

        print(employee_id,password)
        user = employee_login(employee_id, password)

        if user:
            session["employee_id"] = user["employee_id"]
            session["role"] = user["role"]

            if user["role"] == "Manager":
                return redirect(url_for('dashboard_manager'))
            elif user["role"] == "Staff" and user["department"] == "Mainland":
                return redirect(url_for('mainland_tablemanagement'))
            
            elif user["role"] == "Staff" and user["department"] == "Floating Bar":
                return redirect(url_for('cashier_tablemanagement'))
            
            elif user["role"] == "Waiter" and user["department"] == "Floating Bar":
                return redirect(url_for('waiter_tablemanagement'))


        else:
            return render_template("indexv2.html", error="Invalid Login")

    return render_template("indexv2.html")

@app.route("/tablemanagement")
def tablemanagement():
    return render_template("tablemanagement.html")

@app.route("/menu")
def menu():
    main_menu = get_main_menu()
    menu_categories = {}
    for a in main_menu:
        if a['category'] not in menu_categories.keys():
            menu_categories[a['category']] = [a,]
        else:
            menu_categories[a['category']].append(a)
    print(menu_categories)
    return render_template("menu.html", menu_categories=menu_categories)


# @app.route('/process_order/<int:id>', methods=['PUT'])
# def process_order(id):
#     try:
#         data = request.get_json()
#         if not data or "services_availed" not in data:
#             return jsonify({"status": "error", "message": "No services provided"}), 400
#         update_data = {
#             "services_availed": data.get("services_availed"),
#             "table_assigned": data.get("table_assigned"),
#         }

#         result = put_transaction(id=id, data=update_data)

#         return jsonify(result)

#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)})
    
# --------------------------------
#         Arjun WAITER
# -------------------------------
@app.route('/waiter/recreationalactivity')
def waiter_recrational_activity():
    pending_transactions = get_pending_transactions()
    print("Pending transactions: ", pending_transactions)
    return render_template("waiter/recreationalactivity.html", transactions = pending_transactions)


@app.route("/waiter/pending_transactions")
def waiter_pending_transactions():
    pending_transactions = get_pending_transactions()  # Returns a list of dicts
    print("Pending transactions:", pending_transactions)  # Debug line
    return render_template(
        "waiter/pending_transactions.html",
        transactions=pending_transactions
    )


@app.route("/waiter/recreationalctivitymenu/<int:id>")
def recreationactivitymenu(id):
    main_menu = get_recreational_activity()
    txn = get_transaction(id=id)
    menu_categories = {}
    for a in main_menu:
        if a['category'] not in menu_categories.keys():
            menu_categories[a['category']] = [a,]
        else:
            menu_categories[a['category']].append(a)
    print(menu_categories)
    return render_template("/waiter/recreationalctivitymenu.html", menu_categories=menu_categories, txn= txn)



@app.route('/waiter/tablemanagement')
def waiter_tablemanagement():
    tables = get_table()  # get all tables (optional, for layout)
    table_transactions = get_all_table_guest()  # {tableID: txn_dict}

    return render_template(
        "waiter/tablemanagement.html",
        tables=tables,
        table_transactions=table_transactions
    )

@app.route("/waiter/tablemanagementmenu/<int:table_id>")
def tablemanagementmenu(table_id):

    main_menu = get_main_menu()
    txn = get_table_guest(table_id)  # fetch transaction for this ID
    menu_categories = {}
    for a in main_menu:
        if a['category'] not in menu_categories:
            menu_categories[a['category']] = [a]
        else:
            menu_categories[a['category']].append(a)

    print("txn:", txn)
    return render_template("/waiter/tablemanagementmenu.html", menu_categories=menu_categories, txn=txn)





@app.route("/process_order", methods=["POST"])
def process_order():
    data = request.get_json()   

    print(data)

    print("data:",data)
    txn_id = data.get("id")

    if not txn_id:
        return jsonify({"status": "error", "message": "Transaction ID (id) is missing"})

    result = put_transaction(txn_id, {
        "services_availed": data.get("services_availed", []),
        "total_amount_paid": data.get("total_amount_paid"),
        "status": data.get("status")
    })

    return jsonify(result)

# --------------------------------
#         Arjun floating bar cashier
# -------------------------------

@app.route("/cashier/tablemanagement")
def cashier_tablemanagement():
    return render_template("/cashier/tablemanagement.html")

@app.route("/cashier/recreationalactivity")
def cashier_recreationalactivity():
    return render_template("/cashier/recreationalactivity.html")


# --------------------------------
#         Arjun mainland cashier
# -------------------------------
@app.route("/mainland/tablemanagement")
def mainland_tablemanagement():
    tables = get_table()

    deck_prices = {item['deck']: item['price'] for item in get_deck()}

    deck_prices['skydeck'] = deck_prices['skydeck'] - deck_prices['boatride'] - deck_prices['entrancefee']
    deck_prices['maindeck'] = deck_prices['maindeck'] - deck_prices['boatride'] - deck_prices['entrancefee']    

    for row_table in tables:
        if row_table['transaction_id'] is not None:
            transaction = get_transaction_by_transaction_id(row_table['transaction_id'])
            if transaction['status'] == "Pending":
                transaction['totalServicesAvailed'] = 0
                for service in transaction['services_availed'][1:]:
                    transaction['totalServicesAvailed'] += (float(service['unit_price'])*float(service['qty']))
            row_table.update(transaction)

    #print(tables)
    return render_template("/mainland/tablemanagement.html",
                           tables=tables,
                           deck_prices=deck_prices)

@app.route("/mainland/recreationalactivity")
def mainland_recreationalactivity():
    return render_template("/mainland/recreationalactivity.html")





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
