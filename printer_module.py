from PIL import Image
import socket

printer_ip = "192.168.1.220"
port = 9100

ESC = b'\x1b'
GS = b'\x1d'
CUT_SAFE = b'\n\n\n\x1d\x56\x00'


# --------------------------------------------------
# Helpers
# --------------------------------------------------
def money(val):
    return f"{val:,.2f}"

def line():
    return b"------------------------------------------------\n"

def double_line():
    return b"================================================\n"

def item_row(label, value):
    return f"{label:<32}{value:>16}\n".encode()


# --------------------------------------------------
# Receipt Builder
# --------------------------------------------------
def build_receipt(data):
    trx_id = data["transaction_id"]
    table = data["table"]
    guests = data["guests"]

    boat_fee = data["boat_fee"]
    entrance_fee = data["entrance_fee"]
    consumables = data["consumables"]

    total_bill = data["total_bill"]
    discount = data["discount"]
    vat = data["vat"]
    net_total = data["net_total"]
    amount_paid = data["amount_paid"]
    change = data["change"]

    receipt = bytearray()

    receipt += ESC + b'@'                  # Initialize
    receipt += ESC + b'a\x01'              # Center
    receipt += ESC + b'E\x01'              # Bold
    receipt += b"FLOATING BAR\n"
    receipt += ESC + b'E\x00'
    receipt += ESC + b'a\x00'              # Left

    receipt += double_line()
    receipt += f"Transaction ID : {trx_id}\n".encode()
    receipt += f"Table          : {table}\n".encode()
    receipt += f"Guests         : {guests}\n".encode()

    receipt += line()
    receipt += b"ORDER SUMMARY\n"
    receipt += line()

    receipt += item_row("Boat Ride Fee", f"P {money(boat_fee)}")
    receipt += item_row("Entrance Fee", f"P {money(entrance_fee)}")
    receipt += item_row("Consumables", f"P {money(consumables)}")

    receipt += line()
    receipt += ESC + b'E\x01'
    receipt += item_row("TOTAL BILL", f"P {money(total_bill)}")
    receipt += ESC + b'E\x00'

    receipt += b"\nPAYMENT SUMMARY\n"
    receipt += line()

    receipt += item_row("Discount", f"P {money(discount)}")
    receipt += item_row("VAT (12%)", f"P {money(vat)}")

    receipt += ESC + b'E\x01'
    receipt += item_row("NET TOTAL", f"P {money(net_total)}")
    receipt += ESC + b'E\x00'

    receipt += item_row("Amount Paid", f"P {money(amount_paid)}")

    receipt += ESC + b'E\x01'
    receipt += GS + b'!\x11'               # Double size
    receipt += item_row("CHANGE", f"P {money(change)}")
    receipt += GS + b'!\x00'
    receipt += ESC + b'E\x00'

    receipt += line()
    receipt += ESC + b'a\x01'
    receipt += b"Thank you!\n"
    receipt += ESC + b'a\x00'
    receipt += double_line()

    return receipt


# --------------------------------------------------
# Printer Sender
# --------------------------------------------------
def send_to_printer_registration(receipt_bytes, logo_path=None):
    output = bytearray()

    if logo_path:
        image = Image.open(logo_path).convert('1')

        if image.width > 384:
            ratio = 384 / image.width
            new_height = int(image.height * ratio)
            image = image.resize((384, new_height))

        width, height = image.size
        pixels = image.load()

        total_width = 400
        left_padding = 90

        image_data = bytearray()
        image_data += b'\x1d\x76\x30\x00'
        w = (total_width + 7) // 8

        image_data += (w % 256).to_bytes(1, 'little')
        image_data += (w // 256).to_bytes(1, 'little')
        image_data += (height % 256).to_bytes(1, 'little')
        image_data += (height // 256).to_bytes(1, 'little')

        for y in range(height):
            row_bytes = bytearray()
            for x in range(0, w * 8, 8):
                byte = 0
                for bit in range(8):
                    img_x = x - left_padding + bit
                    if 0 <= img_x < width and pixels[img_x, y] == 0:
                        byte |= 1 << (7 - bit)
                row_bytes.append(byte)
            image_data += row_bytes

        output += image_data

    output += receipt_bytes + CUT_SAFE

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((printer_ip, port))
    sock.sendall(output)
    sock.close()

if __name__ == "__main__":
    # --------------------------------------------------
    # Example Usage
    # --------------------------------------------------
    data = {
        "transaction_id": "TRX-8421",
        "table": "SKY12",
        "guests": 8,

        "boat_fee": 4000,
        "entrance_fee": 4000,
        "consumables": 20000,

        "total_bill": 28000,
        "discount": 0,
        "vat": 3360,
        "net_total": 28000,
        "amount_paid": 28000,
        "change": 0.00
    }

    receipt = build_receipt(data)
    send_to_printer_registration(receipt, logo_path="./BlueOceanBar.png")
