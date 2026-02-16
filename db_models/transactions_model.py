
from db_connector import get_connection
import json
from datetime import datetime

# def get_transaction(id=None):
#     conn = get_connection()
#     cursor = conn.cursor(dictionary=True)

#     try:
#         if id:
#             cursor.execute(
#                 "SELECT * FROM transactions WHERE id = %s",
#                 (id,)
#             )
#             return cursor.fetchone()
#         else:
#             cursor.execute("SELECT * FROM transactions")

#             result = cursor.fetchall()
        
#         for row in result:
#             if "services_availed" in row and row["services_availed"]:
#                 row["services_availed"] = json.loads(row["services_availed"])
#             if "add_on_guest" in row and row["add_on_guest"]:
#                 row["add_on_guest"] = json.loads(row["add_on_guest"])
#         return result

#     except Exception as e:
#         return {"status": "error", "message": str(e)}

#     finally:
#         cursor.close()
#         conn.close()
def get_transaction(id=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        if id:
            cursor.execute("SELECT * FROM transactions WHERE id = %s", (id,))
            row = cursor.fetchone()
            # if row:
            #     if "services_availed" in row and row["services_availed"]:
            #         row["services_availed"] = json.loads(row["services_availed"])
            #     if "add_on_guest" in row and row["add_on_guest"]:
            #         row["add_on_guest"] = json.loads(row["add_on_guest"])
            return row
        else:
            cursor.execute("SELECT * FROM transactions")
            result = cursor.fetchall()
            for row in result:
                if "services_availed" in row and row["services_availed"]:
                    row["services_availed"] = json.loads(row["services_availed"])
                if "add_on_guest" in row and row["add_on_guest"]:
                    row["add_on_guest"] = json.loads(row["add_on_guest"])
            return result

    except Exception as e:
        return {"status": "error", "message": str(e)}

    finally:
        cursor.close()
        conn.close()

def get_transaction_by_transaction_id(transaction_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT * FROM transactions WHERE transaction_id = %s",
            (transaction_id,)
        )

        row = cursor.fetchone()

        if row:
            if "services_availed" in row and row["services_availed"]:
                row["services_availed"] = json.loads(row["services_availed"])

            if "add_on_guest" in row and row["add_on_guest"]:
                row["add_on_guest"] = json.loads(row["add_on_guest"])

        return row

    except Exception as e:
        return {"status": "error", "message": str(e)}

    finally:
        cursor.close()
        conn.close()



def post_transaction(data):
    try:
        conn = get_connection()
        cursor = conn.cursor()

    
        services = data.get("services_availed") or []
        
        
        total_billing = sum(float(service.get("unit_price", 0)) for service in services)

       
        discount = float(data.get("discount") or 0.00)

       
        totalnetbilling = total_billing - discount

      
        total_amount_paid = float(data.get("total_amount_paid") or 0.00)

        total_change = total_amount_paid - totalnetbilling

        sql_query = """
        INSERT INTO transactions (
            transaction_id,
            customer_name,
            contact_number,
            table_assigned,
            services_availed,
            add_on_guest,
            total_billing,
            discount,
            totalnetbilling,
            total_amount_paid,
            total_change,
            type_of_payment,
            status,
            created_at
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        values = [
            data.get("transaction_id"),
            data.get("customer_name"),
            data.get("contact_number"),
            data.get("table_assigned"),
            json.dumps(services),
            json.dumps(data.get("add_on_guest")) if data.get("add_on_guest") else None,
            total_billing,
            discount,
            totalnetbilling,
            total_amount_paid,
            total_change,
            data.get("type_of_payment"),
            data.get("status") or "Pending",
            datetime.now()
        ]

        cursor.execute(sql_query, values)

        # Update table status
        if data.get("table_assigned"):
            cursor.execute(
                "UPDATE table_management SET status = 'Pending' WHERE tableID = %s",
                (data.get("table_assigned"),)
            )

        conn.commit()

        return {
            "status": "success",
            "transaction_id": cursor.lastrowid,
            "total_billing": total_billing,
            "totalnetbilling": totalnetbilling,
            "total_change": total_change
        }

    except Exception as e:
        conn.rollback()
        return {"status": "error", "message": str(e)}

    finally:
        cursor.close()
        conn.close()



# def post_transaction(data):
#     try:
#         conn = get_connection()
#         cursor = conn.cursor()

#         sql_query = """
#         INSERT INTO transactions (
#             customer_name,
#             contact_number,
#             table_assigned,
#             services_availed,
#             add_on_guest,
#             total_billing,
#             discount,
#             totalnetbilling,
#             total_amount_paid,
#             total_change,
#             type_of_payment,
#             status,
#             created_at
#         ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
#         """

#         values = [
#             data.get("customer_name"),
#             data.get("contact_number"),
#             data.get("table_assigned"),
#             json.dumps(data.get("services_availed")) if data.get("services_availed") else None,
#             json.dumps(data.get("add_on_guest")) if data.get("add_on_guest") else None,
#             data.get("total_billing"),
#             data.get("discount") or 0.00,
#             data.get("totalnetbilling"),
#             data.get("total_amount_paid"),
#             data.get("total_change"),
#             data.get("type_of_payment"),
#             data.get("status") or "Pending",
#             data.get("created_at") or datetime.now()
#         ]

#         cursor.execute(sql_query, values)

       
#         if data.get("table_assigned"):
#             cursor.execute(
#                 "UPDATE table_management SET status = 'Occupied' WHERE tableID = %s",
#                 (data.get("table_assigned"),)
#             )

#         conn.commit()

#         return {"status": "success", "transaction_id": cursor.lastrowid}

#     except Exception as e:
#         conn.rollback()
#         return {"status": "error", "message": str(e)}

#     finally:
#         cursor.close()
#         conn.close()

def put_transaction(id, data):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

       
        cursor.execute("""
        SELECT customer_name, contact_number,
            services_availed, add_on_guest,
            table_assigned, total_amount_paid,
            discount, status, type_of_payment
        FROM transactions
        WHERE id = %s
        """, (id,))
        existing_row = cursor.fetchone()

        if not existing_row:
            return {"status": "error", "message": "Transaction not found"}

        existing_services = json.loads(existing_row["services_availed"]) if existing_row["services_availed"] else []
        existing_addon = json.loads(existing_row["add_on_guest"]) if existing_row["add_on_guest"] else []

       
        merged_services = existing_services + (data.get("services_availed") or [])
        merged_addon = existing_addon + (data.get("add_on_guest") or [])

       
        total_billing = sum(float(service.get("unit_price", 0)) for service in merged_services)

        
        discount = float(data.get("discount") if data.get("discount") is not None else existing_row.get("discount") or 0.00)
        if discount > total_billing:
            discount = total_billing

        
        totalnetbilling = total_billing - discount

        
        existing_paid = float(existing_row.get("total_amount_paid") or 0.00)
        new_payment = float(data.get("total_amount_paid") or 0.00)
        total_amount_paid = existing_paid + new_payment  

     
        total_change = total_amount_paid - totalnetbilling

  
        new_status = "Completed" if total_amount_paid >= totalnetbilling else "Pending"

   
        new_table = data.get("table_assigned") or existing_row["table_assigned"]

        sql_query = """
        UPDATE transactions
        SET
            transaction_id = %s,
            customer_name = %s,
            contact_number = %s,
            table_assigned = %s,
            services_availed = %s,
            add_on_guest = %s,
            total_billing = %s,
            discount = %s,
            totalnetbilling = %s,
            total_amount_paid = %s,
            total_change = %s,
            type_of_payment = %s,
            status = %s
        WHERE id = %s
        """

        values = [
            data.get("transaction_id") if data.get("transaction_id") is not None else existing_row["transaction_id"],
            data.get("customer_name") if data.get("customer_name") is not None else existing_row["customer_name"],
            data.get("contact_number") if data.get("contact_number") is not None else existing_row["contact_number"],
            new_table,
            json.dumps(merged_services),
            json.dumps(merged_addon),
            total_billing,
            discount,
            totalnetbilling,
            total_amount_paid,
            total_change,
            data.get("type_of_payment") if data.get("type_of_payment") is not None else existing_row["type_of_payment"],
            new_status,
            id
        ]

        cursor.execute(sql_query, values)

      
        if new_status == "Completed":
            cursor.execute(
                "UPDATE table_management SET status = 'Available' WHERE tableID = %s",
                (new_table,)
            )

        conn.commit()

        return {
            "status": "success",
            "updated_rows": cursor.rowcount,
            "computed": {
                "total_billing": total_billing,
                "totalnetbilling": totalnetbilling,
                "total_amount_paid": total_amount_paid,
                "total_change": total_change,
                "status": new_status
            }
        }

    except Exception as e:
        conn.rollback()
        return {"status": "error", "message": str(e)}

    finally:
        cursor.close()
        conn.close()


# def put_amount_paid(id, data):
#     try:
#         conn = get_connection()
#         cursor = conn.cursor(dictionary = True)

#         cursor.execute(
#             """
#             SELECT total_amount_paid FROM transactions WHERE id = %s 
#             """, (id,)
#         )
#         existing_data = cursor.fetchone()

#         if not existing_data:
#             return {"status": "error", "message": "Transaction not Found"}
        
#         new_total_amount_paid = existing_data["total_amount_paid"] + data["total_amount_paid"]

#         cursor.execute(
#             """
#             UPDATE transactions
#             SET
#                 total_amount_paid = %s
#             WHERE id = %s
#             """,
#             (new_total_amount_paid, id)
#         )
#         conn.commit()
#         return {
#             "status": "success",
#             "updated_rows": cursor.rowcount,
#             "total_amount_paid": new_total_amount_paid
#         }
    

    # except Exception as e:
    #     conn.rollback()
    #     return {"status": "error", "message": str(e)}
    # finally:
    #     cursor.close()
    #     conn.close()


# def put_transaction(id, data):

#     try:
#         conn = get_connection()
#         cursor = conn.cursor(dictionary=True)

      
#         cursor.execute("""
#             SELECT services_availed, add_on_guest, table_assigned, status
#             FROM transactions WHERE id = %s
#         """, (id,))
#         existing_row = cursor.fetchone()

#         if not existing_row:
#             return {"status": "error", "message": "Transaction not found"}

#         existing_services = json.loads(existing_row["services_availed"]) if existing_row["services_availed"] else []
#         existing_addon = json.loads(existing_row["add_on_guest"]) if existing_row["add_on_guest"] else []

#         merged_services = existing_services + (data.get("services_availed") or [])
#         merged_addon = existing_addon + (data.get("add_on_guest") or [])

#         sql_query = """
#         UPDATE transactions
#         SET
#             customer_name = %s,
#             contact_number = %s,
#             table_assigned = %s,
#             services_availed = %s,
#             add_on_guest = %s,
#             total_billing = %s,
#             discount = %s,
#             totalnetbilling = %s,
#             total_amount_paid = %s,
#             total_change = %s,
#             type_of_payment = %s,
#             status = %s
#         WHERE id = %s
#         """

#         new_status = data.get("status") or existing_row["status"]
#         new_table = data.get("table_assigned") or existing_row["table_assigned"]

#         values = [
#             data.get("customer_name"),
#             data.get("contact_number"),
#             new_table,
#             json.dumps(merged_services),
#             json.dumps(merged_addon),
#             data.get("total_billing"),
#             data.get("discount") or 0.00,
#             data.get("totalnetbilling"),
#             data.get("total_amount_paid"),
#             data.get("total_change"),
#             data.get("type_of_payment"),
#             new_status,
#             id
#         ]

#         cursor.execute(sql_query, values)

#         if new_status == "Completed":
#             cursor.execute(
#                 "UPDATE table_management SET status = 'Available' WHERE tableID = %s",
#                 (new_table,)
#             )

#         conn.commit()

#         return {"status": "success", "updated_rows": cursor.rowcount}

#     except Exception as e:
#         conn.rollback()
#         return {"status": "error", "message": str(e)}

#     finally:
#         cursor.close()
#         conn.close()



def delete_transaction(id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM transactions WHERE id = %s",
            (id,)
        )
        conn.commit()

        return {"status": "Successfully Deleted", "deleted_rows": cursor.rowcount}

    except Exception as e:
        conn.rollback()
        return {"status": "error", "message": str(e)}

    finally:
        cursor.close()
        conn.close()