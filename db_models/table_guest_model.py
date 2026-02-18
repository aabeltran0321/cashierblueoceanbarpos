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
        # rows = cursor.fetchone()

    
        row = cursor.fetchone()

        if row:
            if row["services_availed"]:
                row["services_availed"] = json.loads(row["services_availed"])
            if row["add_on_guest"]:
                row["add_on_guest"] = json.loads(row["add_on_guest"])

        return row


    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        cursor.close()
        conn.close()

def get_all_table_guest():
    """
    Get all transactions that have a table assigned.
    Returns a dictionary keyed by tableID for easy lookup in Jinja.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        sql = """
            SELECT *
            FROM transactions
            WHERE table_assigned IS NOT NULL
            AND status = "Pending"
        """
        cursor.execute(sql)
        rows = cursor.fetchall()

        # Decode JSON fields if they exist
        for row in rows:
            if "services_availed" in row and row["services_availed"]:
                row["services_availed"] = json.loads(row["services_availed"])
            if "add_on_guest" in row and row["add_on_guest"]:
                row["add_on_guest"] = json.loads(row["add_on_guest"])

        # Convert list to dictionary keyed by tableID
        table_dict = {}
        for row in rows:
            remaining = float(row.get("totalnetbilling", 0)) - float(row.get("total_amount_paid", 0))
            table_dict[row["table_assigned"]] = {
                "transaction_id": row.get("transaction_id"),
                "total": row.get("totalnetbilling", 0),
                "total_amount_paid": row.get("total_amount_paid"),
                "remaining": remaining,
                "status": row.get("status", "Pending")
            }

        return table_dict

    except Exception as e:
        return {"status": "error", "message": str(e)}

    finally:
        cursor.close()
        conn.close()