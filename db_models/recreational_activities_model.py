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
            price,
            picture_url,
            status
        ) VALUES (%s,%s,%s,%s)
        """

        values = [
            activity_data.get("activity_name"),
            activity_data.get("price"),
            activity_data.get("picture_url"),
            activity_data.get("status") or "Available"
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
            price = %s,
            picture_url = %s,
            status = %s
        WHERE id = %s
        """

        values = [
            activity_data.get("activity_name"),
            activity_data.get("price"),
            activity_data.get("picture_url"),
            activity_data.get("status") or "Available",
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
