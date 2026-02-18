from db_connector import get_connection


# =========================
# GET (single or all)
# =========================
def get_recreational_activity(activity_id=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        if activity_id:
            cursor.execute(
                "SELECT * FROM recreational_activities WHERE id = %s",
                (activity_id,)
            )
        else:
            cursor.execute("SELECT * FROM recreational_activities")

        result = cursor.fetchall()
        return result

    except Exception as e:
        return {"status": "error", "message": str(e)}

    finally:
        cursor.close()
        conn.close()
def get_recreational_activities_with_transaction():
    """
    Fetch all recreational activities that have a non-null transaction_id.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT *
            FROM recreational_activities
            WHERE transaction_id IS NOT NULL
        """)

        result = cursor.fetchall()
        return result

    except Exception as e:
        return {"status": "error", "message": str(e)}

    finally:
        cursor.close()
        conn.close()


# =========================
# POST (create activity)
# =========================
def post_recreational_activity(activity_data):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql_query = """
        INSERT INTO recreational_activities (
            activity_name,
            unit_price,
            picture_url,
            status,
            category
        ) VALUES (%s,%s,%s,%s,%s)
        """

        values = [
            activity_data.get("activity_name"),
            activity_data.get("unit_price"),
            activity_data.get("picture_url"),
            activity_data.get("status") or "Available",
            activity_data.get("category")
        ]

        cursor.execute(sql_query, values)
        conn.commit()

        return {"status": "success", "id": cursor.lastrowid}

    except Exception as e:
        conn.rollback()
        return {"status": "error", "message": str(e)}

    finally:
        cursor.close()
        conn.close()


# =========================
# PUT (update activity)
# =========================
def put_recreational_activity(activity_id, activity_data):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql_query = """
        UPDATE recreational_activities
        SET
            activity_name = %s,
            unit_price = %s,
            picture_url = %s,
            status = %s,
            category = %s
        WHERE id = %s
        """

        values = [
            activity_data.get("activity_name"),
            activity_data.get("unit_price"),
            activity_data.get("picture_url"),
            activity_data.get("status") or "Available",
            activity_data.get("category"),
    
            activity_id
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


def put_recreational_activity_transaction_status(id, transaction_id=None):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Always set status to "Occupied"
        status = "Occupied"

        # transaction_id can be None if not provided
        sql_query = """
        UPDATE recreational_activities
        SET
            status = %s,
            transaction_id = %s
        WHERE id = %s
        """

        values = (status, transaction_id, id)

        cursor.execute(sql_query, values)
        conn.commit()

        return {
            "status": "success",
            "activity_status": status,
            "updated_rows": cursor.rowcount,
            "transaction_id": transaction_id
        }

    except Exception as e:
        conn.rollback()
        return {"status": "error", "message": str(e)}

    finally:
        cursor.close()
        conn.close()

# =========================
# DELETE
# =========================
def delete_recreational_activity(activity_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM recreational_activities WHERE id = %s",
            (activity_id,)
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
