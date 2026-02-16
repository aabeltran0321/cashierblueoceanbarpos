from db_connector import get_connection


def get_order(order_id = None):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        if order_id:
            cursor.execute("SELECT * FROM orders WHERE order_id = %s", (order_id,))
        else:
            cursor.execute("SELECT * FROM orders")

        result = cursor.fetchall()
        return result

    except Exception as e:
        return {"status": "error", "message" : str(e)}
    finally:
        cursor.close()
        conn.close()

def post_order(order_data):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql_query = """
            INSERT INTO orders(
                name,
                category,
                unit_price,
                status
            ) VALUES(%s, %s, %s, %s)
        """
        values = [
            order_data.get("name"),
            order_data.get("category"),
            order_data.get("unit_price"),
            order_data.get("status") or "Pending"  # default to Pending if not provided
        ]
        cursor.execute(sql_query, values)
        conn.commit()
        return {"status": "success", "order_id": cursor.lastrowid}

    except Exception as e:
        conn.rollback()
        return {"status": "error", "message": str(e)}

    finally:
        cursor.close()
        conn.close()


def put_order(order_id, order_data):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql_query = """
            UPDATE orders
            SET
                name = %s,
                category = %s,
                unit_price = %s,
                status = %s
            WHERE order_id = %s
        """
        values = [
            order_data.get("name"),
            order_data.get("category") ,
            order_data.get("unit_price"),
            order_data.get("status") or "Pending",
            order_id
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


def delete_order(order_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM orders WHERE order_id = %s", (order_id,))
        conn.commit()

        return {"status": "success", "deleted_rows": cursor.rowcount}

    except Exception as e:
        conn.rollback()
        return {"status": "error", "message": str(e)}

    finally:
        cursor.close()
        conn.close()