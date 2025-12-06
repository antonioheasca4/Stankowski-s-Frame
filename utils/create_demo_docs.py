"""
Demo Document Generator
Creates sample documents for demonstration purposes
"""

from PIL import Image, ImageDraw, ImageFont
import os


def create_sample_document(amount: str, output_path: str, logo_path: str = None):
    """
    Create a sample Deutsche Bank document
    
    Args:
        amount: Amount to display on document
        output_path: Where to save the document
        logo_path: Path to Deutsche Bank logo
    """
    # Create a white canvas
    width, height = 800, 1000
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    # Try to use a nice font, fallback to default
    try:
        title_font = ImageFont.truetype("arial.ttf", 36)
        header_font = ImageFont.truetype("arial.ttf", 24)
        text_font = ImageFont.truetype("arial.ttf", 18)
        amount_font = ImageFont.truetype("arialbd.ttf", 48)
    except:
        title_font = ImageFont.load_default()
        header_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        amount_font = ImageFont.load_default()
    
    # Add Deutsche Bank logo if available
    if logo_path and os.path.exists(logo_path):
        try:
            logo = Image.open(logo_path)
            # Resize logo to reasonable size
            logo_width = 150
            logo_height = int(logo.size[1] * (logo_width / logo.size[0]))
            logo = logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
            
            # Paste logo in top-left
            img.paste(logo, (50, 50), logo if logo.mode == 'RGBA' else None)
        except Exception as e:
            print(f"Could not load logo: {e}")
    
    # Draw header
    draw.rectangle([0, 0, width, 180], fill='#0018A8')
    
    # Add "Deutsche Bank" text (if no logo or as additional header)
    db_text = "DEUTSCHE BANK"
    try:
        draw.text((250, 60), db_text, fill='white', font=title_font)
    except:
        draw.text((250, 60), db_text, fill='white')
    
    # Document title
    y_pos = 220
    draw.text((50, y_pos), "CONTRACT AGREEMENT", fill='#0018A8', font=header_font)
    
    # Document details
    y_pos += 80
    draw.text((50, y_pos), "Contract No: DB-2025-001234", fill='black', font=text_font)
    
    y_pos += 40
    draw.text((50, y_pos), "Date: December 6, 2025", fill='black', font=text_font)
    
    y_pos += 40
    draw.text((50, y_pos), "IBAN: DE89370400440532013000", fill='black', font=text_font)
    
    # Amount section (the critical part)
    y_pos += 100
    draw.rectangle([50, y_pos, width-50, y_pos+150], outline='#0018A8', width=3)
    
    y_pos += 20
    draw.text((70, y_pos), "TOTAL AMOUNT:", fill='#0018A8', font=header_font)
    
    y_pos += 50
    amount_text = f"{amount} EUR"
    draw.text((70, y_pos), amount_text, fill='#000000', font=amount_font)
    
    # Terms and conditions
    y_pos += 150
    draw.text((50, y_pos), "Terms and Conditions:", fill='black', font=header_font)
    
    y_pos += 40
    terms = [
        "This contract is valid for the specified amount only.",
        "Any modification to this document invalidates the contract.",
        "Deutsche Bank AG - Frankfurt am Main",
        "Secured by Stankowski's Frame Technology"
    ]
    
    for term in terms:
        draw.text((50, y_pos), f"• {term}", fill='#333333', font=text_font)
        y_pos += 35
    
    # Footer
    draw.rectangle([0, height-60, width, height], fill='#0018A8')
    draw.text((50, height-45), "Deutsche Bank AG © 2025", fill='white', font=text_font)
    
    # Save
    img.save(output_path, quality=100, subsampling=0)
    print(f"✓ Created sample document: {output_path}")


def create_demo_documents():
    """Create demo documents for the presentation"""
    
    print("Creating demo documents...")
    print("=" * 50)
    
    # Check if logo exists
    logo_path = "deutsche_bank_logo.png"
    
    if not os.path.exists(logo_path):
        print(f"⚠️  Warning: {logo_path} not found. Creating documents without logo.")
        print("   Please add your Deutsche Bank logo as 'deutsche_bank_logo.png'")
        logo_path = None
    
    # Create authentic document (10,000 EUR)
    create_sample_document("10,000", "demo_authentic.png", logo_path)
    
    # Create fraudulent document (50,000 EUR - will be detected as fraud)
    create_sample_document("50,000", "demo_fraudulent.png", logo_path)
    
    print("\n" + "=" * 50)
    print("Demo documents created successfully!")
    print("\nNext steps:")
    print("1. Use the Encoder to secure 'demo_authentic.png' with amount=10000")
    print("2. Then test fraud detection by uploading it to Decoder with visible_amount=50000")


if __name__ == "__main__":
    create_demo_documents()
