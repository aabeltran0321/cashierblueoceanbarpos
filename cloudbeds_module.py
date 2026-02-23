import requests

token_key = "cbat_ytHoA2RACmuxpTP9TcdSJdPUS4JjreuN"
def get_reservations():
    url = "https://api.cloudbeds.com/api/v1.3/getReservations"

    headers = {
        "accept": "application/json",
        "x-api-key": token_key
    }

    response = requests.get(url, headers=headers)

    return response.json()

def getRooms():

    url = "https://api.cloudbeds.com/api/v1.3/getRooms"

    headers = {
        "accept": "application/json",
        "x-api-key": token_key
    }

    response = requests.get(url, headers=headers)

    return response.json()

def get_reservation_by_id(reservationID:str):
    url = f"https://api.cloudbeds.com/api/v1.3/getReservation?reservationID={reservationID}"

    headers = {
        "accept": "application/json",
        "x-api-key": token_key
    }

    response = requests.get(url, headers=headers)

    return response.json()





def extract_reservation_details(reservation_response, rooms_response):
    reservation = reservation_response["data"]
    guest_list = reservation["guestList"]

    main_guest = None
    add_on_guests = []

    # -------------------------
    # Extract Guests
    # -------------------------
    for guest_id, guest in guest_list.items():
        full_name = f'{guest["guestFirstName"]} {guest["guestLastName"]}'
        contact = guest["guestPhone"] or guest["guestCellPhone"]

        guest_info = {
            "name": full_name,
            "email": guest["guestEmail"],
            "contact": contact
        }

        if guest["isMainGuest"]:
            main_guest = guest_info
        else:
            add_on_guests.append(guest_info)

    # -------------------------
    # Extract Room Assignment
    # -------------------------
    assigned_room = reservation["assigned"][0]

    room_id = assigned_room["roomID"]

    # -------------------------
    # Find Seating Capacity
    # -------------------------
    seating_info = get_seating_capacity(room_id, rooms_response)

    # -------------------------
    # Build Final Object
    # -------------------------
    result = {
        "reservation_id": reservation["reservationID"],
        "status": reservation["status"],

        "check_in_date": reservation["startDate"],
        "check_out_date": reservation["endDate"],

        "amount_paid": reservation["balanceDetailed"]["paid"],

        "main_guest": main_guest,
        "add_on_guests": add_on_guests,

        "room": {
            "room_id": room_id,
            "room_name": seating_info["room_name"],
            "room_type_id": seating_info["room_type_id"],
            "room_type_name": seating_info["room_type_name"],
            "capacity": seating_info["capacity"]
        }
    }

    return result


def get_seating_capacity(room_id, rooms_response):
    rooms = rooms_response["data"][0]["rooms"]

    for room in rooms:
        if room["roomID"] == room_id:
            return {
                "capacity": room["maxGuests"],
                "room_name": room["roomName"],
                "room_type_id": room["roomTypeID"],
                "room_type_name": room["roomTypeName"]
            }

    return {
        "capacity": 0,
        "room_name": "Unknown",
        "room_type_id": None,
        "room_type_name": "Unknown"
    }


# ---------------------------------------------------
# Example Usage
# ---------------------------------------------------


for row in get_reservations()['data']:
    reservationID = row['reservationID']
    #roomID = row['roomID']

    reservation_response = get_reservation_by_id(reservationID)
    if len(reservation_response['data']['assigned']):
        print(reservation_response['data']['unassigned'])
        rooms_response = get_seating_capacity()

        data = extract_reservation_details(reservation_response, rooms_response)

        print(data)