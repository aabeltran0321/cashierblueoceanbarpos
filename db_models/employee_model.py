from db_connector import get_connection


def get_employee(id=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        if id:
            cursor.execute(
                "SELECT * FROM employee_management WHERE id = %s",
                (id,)
            )
        else:
            cursor.execute("SELECT * FROM employee_management")

        result = cursor.fetchall()
        return result

    except Exception as e:
        return {"status": "error", "message": str(e)}

    finally:
        cursor.close()
        conn.close()

def post_employee(employee_data):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql_query = """
        INSERT INTO employee_management (
            employee_id,
            password,
            firstName,
            lastName,
            role,
            contact_number,
            email,
            status,
            department
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s, %s)
        """

        values = [
            employee_data.get("employee_id"),
            employee_data.get("password"),
            employee_data.get("firstName"),
            employee_data.get("lastName"),
            employee_data.get("role"),
            employee_data.get("contact_number"),
            employee_data.get("email"),
            employee_data.get("status") or "Active",
            employee_data.get("department")
        ]

        cursor.execute(sql_query, values)
        conn.commit()

        return {"status": "success", "employee_id": cursor.lastrowid}

    except Exception as e:
        conn.rollback()
        return {"status": "error", "message": str(e)}

    finally:
        cursor.close()
        conn.close()

def put_employee(id, employee_data):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql_query = """
        UPDATE employee_management
        SET
            employee_id = %s,
            password = %s,
            firstName = %s,
            lastName = %s,
            role = %s,
            contact_number = %s,
            email = %s,
            status = %s,
            department = %s
        WHERE id = %s
        """

        values = [
            employee_data.get("employee_id"),
            employee_data.get("password"),
            employee_data.get("firstName"),
            employee_data.get("lastName"),
            employee_data.get("role"),
            employee_data.get("contact_number"),
            employee_data.get("email"),
            employee_data.get("status"),
            employee_data.get("department"),
            id
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

def delete_employee(id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM employee_management WHERE id = %s",
            (id,)
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
