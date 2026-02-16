from db_connector import get_connection


# =========================
# GET (single or all tables)
# =========================
def get_table(tableID=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        if tableID:
            cursor.execute(
                "SELECT * FROM table_management WHERE tableID = %s",
                (tableID,)
            )
        else:
            cursor.execute("SELECT * FROM table_management")

        result = cursor.fetchall()
        return result

    except Exception as e:
        return {"status": "error", "message": str(e)}

    finally:
        cursor.close()
        conn.close()


# =========================
# POST (create a table)
# =========================
def post_table(table_data):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql_query = """
        INSERT INTO table_management (
            tableName,
            capacity,
            location,
            status
        ) VALUES (%s, %s, %s, %s)
        """

        values = [
            table_data.get("tableName"),
            table_data.get("capacity"),
            table_data.get("location"),
            table_data.get("status") or "Available"
        ]

        cursor.execute(sql_query, values)
        conn.commit()

        return {"status": "success", "tableID": cursor.lastrowid}

    except Exception as e:
        conn.rollback()
        return {"status": "error", "message": str(e)}

    finally:
        cursor.close()
        conn.close()


# =========================
# PUT (update a table)
# =========================
def put_table(tableID, table_data):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql_query = """
        UPDATE table_management
        SET
            tableName = %s,
            capacity = %s,
            location = %s,
            status = %s
        WHERE tableID = %s
        """

        values = [
            table_data.get("tableName"),
            table_data.get("capacity"),
            table_data.get("location"),
            table_data.get("status"),
            tableID
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
# DELETE (remove a table)
# =========================
def delete_table(tableID):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM table_management WHERE tableID = %s",
            (tableID,)
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
