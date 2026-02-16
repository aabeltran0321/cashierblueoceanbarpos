from db_connector import get_connection

def employee_login(employee_id, password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM employee_management WHERE employee_id = %s AND password = %s",
        (employee_id, password)
    )
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result