import qrcode
import io

def generate_qr_bytes(data):
    """Generates a QR code and returns its raw bytes in-memory."""
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save image to a memory buffer instead of writing a file to disk
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()
