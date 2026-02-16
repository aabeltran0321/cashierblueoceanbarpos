from db_connector import get_connection
import json

def get_table_guest(tableID):
    if not tableID:
        return []  

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        sql = """
            SELECT *
            FROM transactions
            WHERE table_assigned = %s AND 
            status = "Pending"
        """
        cursor.execute(sql, (tableID,))
        rows = cursor.fetchall()

    
        for row in rows:
            if "services_availed" in row and row["services_availed"]:
                row["services_availed"] = json.loads(row["services_availed"])
            if "add_on_guest" in row and row["add_on_guest"]:
                row["add_on_guest"] = json.loads(row["add_on_guest"])

        return rows

    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        cursor.close()
        conn.close()