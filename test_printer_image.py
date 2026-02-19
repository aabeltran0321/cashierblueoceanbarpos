from PIL import Image
import socket

printer_ip = "192.168.1.220"
port = 9100

ESC = b'\x1b'
GS = b'\x1d'
CUT_SAFE = b'\n\n\n\x1d\x56\x00'  # Safe cut: feed + full cut

# -----------------------------
# Step 1: Prepare logo image
# -----------------------------
image = Image.open("./BlueOceanBar.png").convert('1')  # Convert to 1-bit

# Resize if wider than 384px
if image.width > 384:
    ratio = 384 / image.width
    new_height = int(image.height * ratio)
    image = image.resize((384, new_height))

# Centering: calculate left padding
total_width = 400
left_padding = 90



width, height = image.size
pixels = image.load()

# Convert image to ESC/POS raster bytes (with left padding for centering)
image_data = bytearray()
image_data += b'\x1d\x76\x30\x00'  # GS v 0 m=0
w = (total_width + 7) // 8
image_data += (w % 256).to_bytes(1, 'little')
image_data += (w // 256).to_bytes(1, 'little')
image_data += (height % 256).to_bytes(1, 'little')
image_data += (height // 256).to_bytes(1, 'little')

for y in range(height):
    row_bytes = bytearray()
    for x in range(0, w*8, 8):
        byte = 0
        for bit in range(8):
            img_x = x - left_padding + bit
            if 0 <= img_x < width and pixels[img_x, y] == 0:
                byte |= 1 << (7 - bit)
        row_bytes.append(byte)
    image_data += row_bytes

# -----------------------------
# Step 2: Prepare text receipt
# -----------------------------
text_receipt = (
    ESC + b'@' +                      # Initialize
    ESC + b'a\x01' +                   # Center align
    ESC + b'E\x01' +                   # Bold header
    b"FLOATING BAR\n" +
    ESC + b'E\x00' +
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
    + ESC + b'E\x01'                    # Bold TOTAL
    + GS + b'!\x11'                     # Double size text
    + b"TOTAL: 680.00\n"
    + GS + b'!\x00'                     # Normal size
    + ESC + b'E\x00'                    # Bold OFF
    + b"------------------------------------------------\n"
    b"Payment Method : Consumables\n"
    b"Remaining Bal. : 1,320.00\n"
    b"------------------------------------------------\n\n"
    + ESC + b'a\x01'                     # Center footer
    + b"Enjoy your stay!\n"
    + ESC + b'a\x00'                     # Left align
    + b"================================================\n"
)

# -----------------------------
# Step 3: Send to printer
# -----------------------------
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((printer_ip, port))
sock.sendall(image_data + text_receipt + CUT_SAFE)
sock.close()
