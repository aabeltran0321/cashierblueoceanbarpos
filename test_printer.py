import socket

printer_ip = "192.168.1.223"
port = 9100

ESC = b'\x1b'
GS = b'\x1d'
CUT_SAFE = b'\n\n\n\x1d\x56\x00'

# Build the receipt as one bytes object
receipt = (
    ESC + b'@' +                      # Initialize printer
    ESC + b'a\x01' +                   # Center align
    ESC + b'E\x01' +                   # Bold ON
    b"FLOATING BAR\n" +
    ESC + b'E\x00' +                   # Bold OFF
    ESC + b'a\x00' +                   # Left align
    b"================================================\n"
    b"Transaction ID : TRX-8421\n"
    b"Table          : SKY12\n"
    b"Guests         : 4\n"
    b"------------------------------------------------\n"
    b"ITEMS\n"
    b"------------------------------------------------\n"
    b"2  San Mig Light                    180.00\n"
    b"1  Mojito                           220.00\n"
    b"1  Sisig                            280.00\n"
    b"------------------------------------------------\n"
    + ESC + b'E\x01'                    # Bold ON for TOTAL
    + GS + b'!\x11'                     # Double size text
    + b"TOTAL: 680.00\n"
    + GS + b'!\x00'                     # Normal size text
    + ESC + b'E\x00'                    # Bold OFF
    + b"------------------------------------------------\n"
    b"Payment Method : Consumables\n"
    b"Remaining Bal. : 1,320.00\n"
    b"------------------------------------------------\n\n"
    + ESC + b'a\x01'                     # Center align footer
    + b"Enjoy your stay!\n"
    + ESC + b'a\x00'                     # Left align
    + b"================================================\n"
)

# Send to printer
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((printer_ip, port))
sock.sendall(receipt + CUT_SAFE)
sock.close()
