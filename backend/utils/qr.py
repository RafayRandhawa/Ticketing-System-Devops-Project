"""
Utility functions for QR code generation
"""

import qrcode
from io import BytesIO
from pathlib import Path
import base64

def generate_qr_code(data: str, size: int = 10, border: int = 4) -> str:
    """
    Generate QR code and return as base64 string
    
    Args:
        data: Data to encode in QR code
        size: Size of QR code
        border: Border size
    
    Returns:
        Base64 encoded QR code image
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=size,
        border=border,
    )
    
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/png;base64,{qr_base64}"

def save_qr_code(data: str, filename: str, directory: str = "qr_codes") -> str:
    """
    Save QR code to file
    
    Args:
        data: Data to encode
        filename: Filename for QR code
        directory: Directory to save QR code
    
    Returns:
        Path to saved QR code
    """
    # Create directory if it doesn't exist
    Path(directory).mkdir(parents=True, exist_ok=True)
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    filepath = Path(directory) / f"{filename}.png"
    img.save(str(filepath))
    
    return str(filepath)
