from db_connector import get_connection


def get_deck(id = None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        if id:
            cursor.execute("SELECT * FROM decks WHERE id = %s", (id,))
        else:
            cursor.execute("SELECT * FROM decks")

        result = cursor.fetchall()
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}

    finally:
        cursor.close()
        conn.close()

def post_deck(deck_data):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql_query = """
            INSERT INTO decks(
                deck,
                price
            ) VALUES(%s, %s)

            """
        values = [
            deck_data.get("deck"),
            deck_data.get("price")
        ]
        cursor.execute(sql_query,values)
        conn.commit()
        return {"status": "success", "id": cursor.lastrowid}

    except Exception as e:
        conn.rollback()
        return {"status": "error", "message": str(e)}

    finally:
        cursor.close()
        conn.close()    


def put_deck(id, deck_data):
    try:
        conn =get_connection()
        cursor = conn.cursor()

        sql_query = """
            UPDATE decks
            SET
                deck = %s,
                price = %s
            WHERE id  = %s
            """
        values = [
            deck_data.get("deck"),
            deck_data.get("price"),
            id]

        cursor.execute(sql_query, values)
        conn.commit()

        return {"status": "success", "updated_rows": cursor.rowcount}
    except Exception as e:
        conn.rollback()
        return {"status": "error", "message": str(e)}

    finally:
        cursor.close()
        conn.close()


def delete_deck(id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM decks WHERE id = %s", (id,))
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
