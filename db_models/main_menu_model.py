from db_connector import get_connection


# =========================
# GET (single or all)
# =========================
def get_main_menu(menu_id=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        if menu_id:
            cursor.execute(
                "SELECT * FROM main_menu_management WHERE menu_id = %s",
                (menu_id,)
            )
        else:
            cursor.execute("SELECT * FROM main_menu_management")

        result = cursor.fetchall()
        return result

    except Exception as e:
        return {"status": "error", "message": str(e)}

    finally:
        cursor.close()
        conn.close()

def get_main_menu_category(category):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        if category:
            cursor.execute("SELECT * FROM main_menu_management WHERE category = %s", (category,))
            result = cursor.fetchall()

            return result
    except Exception as e:
        return {"status": "error", "message": str(e)}

    finally:
        cursor.close()
        conn.close()

# =========================
# POST (create menu item)
# =========================
def post_main_menu(menu_data):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql_query = """
        INSERT INTO main_menu_management (
            menu_name,
            category,
            kitchen_printer,
            unit_price,
            picture_url
        ) VALUES (%s,%s,%s,%s,%s)
        """

        values = [
            menu_data.get("menu_name"),
            menu_data.get("category"),
            menu_data.get("kitchen_printer"),
            menu_data.get("unit_price"),
            menu_data.get("picture_url")
        ]

        cursor.execute(sql_query, values)
        conn.commit()

        return {"status": "success", "menuid": cursor.lastrowid}

    except Exception as e:
        conn.rollback()
        return {"status": "error", "message": str(e)}

    finally:
        cursor.close()
        conn.close()



# =========================
# PUT (update menu item)
# =========================
def put_main_menu(menuid, menu_data):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql_query = """
        UPDATE main_menu_management
        SET
            menu_name = %s,
            category = %s,
            kitchen_printer = %s,
            unit_price = %s,
            picture_url = %s
        WHERE menu_id = %s
        """

        values = [
            menu_data.get("menu_name"),
            menu_data.get("category"),
            menu_data.get("kitchen_printer"),
            menu_data.get("unit_price"),
            menu_data.get("picture_url"),
            menuid
        ]

        cursor.execute(sql_query, values)
        conn.commit()

        return {"status": "success", "updated_rows": cursor.rowcount}

    except Exception as e:
        conn.rollback()
        return {"status": "error", "message": str(e)}

    finally:
        cursor.close()
        conn.close()



# =========================
# DELETE
# =========================
def delete_main_menu(menu_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM main_menu_management WHERE menu_id = %s",
            (menu_id,)
        )

        conn.commit()

        return {
            "status": "Successfully Deleted",
            "deleted_rows": cursor.rowcount
        }

    except Exception as e:
        conn.rollback()
        return {"status": "error", "message": str(e)}

    finally:
        cursor.close()
        conn.close()
