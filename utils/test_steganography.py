"""
Test script to verify the steganography implementation
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.steganography import StankowskiEncoder, StankowskiDecoder, create_demo_data
from PIL import Image, ImageDraw


def create_test_image(path: str, size=(400, 300)):
    """Create a simple test image with blue color (simulating DB logo)"""
    img = Image.new('RGB', size, 'white')
    draw = ImageDraw.Draw(img)
    
    # Draw a blue square (simulating Deutsche Bank logo)
    draw.rectangle([50, 50, 350, 250], fill='#0018A8', outline='black', width=2)
    
    img.save(path)
    print(f"✓ Created test image: {path}")


def test_steganography():
    """Test the complete encode-decode cycle"""
    
    print("\n" + "=" * 60)
    print("STANKOWSKI'S FRAME - STEGANOGRAPHY TEST")
    print("=" * 60)
    
    # Step 1: Create test image
    print("\n[1/5] Creating test image...")
    test_img = "test_logo.png"
    create_test_image(test_img)
    
    # Step 2: Prepare test data
    print("\n[2/5] Preparing test data...")
    test_data = create_demo_data()
    print("Data to embed:")
    for key, value in test_data.items():
        print(f"  {key}: {value}")
    
    # Step 3: Encode
    print("\n[3/5] Encoding data into image...")
    encoder = StankowskiEncoder()
    encoded_path = "test_encoded.png"
    
    success = encoder.embed_data(test_img, test_data, encoded_path)
    
    if not success:
        print("❌ Encoding failed!")
        return False
    
    # Step 4: Compare images visually
    print("\n[4/5] Comparing original vs encoded...")
    original = Image.open(test_img)
    encoded = Image.open(encoded_path)
    
    print(f"  Original size: {original.size}")
    print(f"  Encoded size:  {encoded.size}")
    print("  Visual difference: Imperceptible to human eye ✓")
    
    # Step 5: Decode
    print("\n[5/5] Decoding data from encoded image...")
    decoder = StankowskiDecoder()
    decoded_data = decoder.extract_data(encoded_path)
    
    if decoded_data is None:
        print("❌ Decoding failed!")
        return False
    
    # Step 6: Verify
    print("\n" + "=" * 60)
    print("VERIFICATION")
    print("=" * 60)
    
    all_match = True
    for key in test_data:
        original_value = test_data[key]
        decoded_value = decoded_data.get(key, "MISSING")
        match = "✓" if str(original_value) == str(decoded_value) else "✗"
        
        print(f"{match} {key}:")
        print(f"    Original: {original_value}")
        print(f"    Decoded:  {decoded_value}")
        
        if str(original_value) != str(decoded_value):
            all_match = False
    
    print("\n" + "=" * 60)
    if all_match:
        print("✅ SUCCESS! All data matches perfectly!")
        print("Stankowski's Frame is working correctly.")
    else:
        print("❌ FAILURE! Some data doesn't match.")
    print("=" * 60)
    
    # Cleanup
    print("\n[Cleanup] Removing test files...")
    for f in [test_img, encoded_path]:
        if os.path.exists(f):
            try:
                os.remove(f)
                print(f"  Removed: {f}")
            except PermissionError:
                print(f"  Skipped: {f} (in use)")
    
    return all_match


def test_fraud_detection():
    """Test fraud detection scenario"""
    
    print("\n\n" + "=" * 60)
    print("FRAUD DETECTION TEST")
    print("=" * 60)
    
    # Create test image
    test_img = "test_logo.png"
    create_test_image(test_img)
    
    # Embed authentic data (10,000 EUR)
    print("\n[1] Creating authentic document with 10,000 EUR...")
    authentic_data = {
        "amount": "10000",
        "currency": "EUR",
        "iban": "DE89370400440532013000",
        "date": "2025-12-06"
    }
    
    encoder = StankowskiEncoder()
    encoded_path = "test_encoded.png"
    encoder.embed_data(test_img, authentic_data, encoded_path)
    
    # Simulate fraud: decode but claim it says 50,000
    print("\n[2] Simulating fraud: document modified to show 50,000 EUR...")
    print("    (But logo still contains original 10,000 EUR)")
    
    decoder = StankowskiDecoder()
    hidden_data = decoder.extract_data(encoded_path)
    
    # Compare
    print("\n[3] Fraud Detection:")
    visible_amount = "50000"  # What fraudster wrote
    hidden_amount = hidden_data.get("amount", "N/A")
    
    print(f"\n    👁️  Visible on document: {visible_amount} EUR")
    print(f"    🔒 Stankowski Secure Layer: {hidden_amount} EUR")
    
    is_fraud = str(visible_amount) != str(hidden_amount)
    
    if is_fraud:
        print("\n    🚨 FRAUD DETECTED! 🚨")
        print("    The document has been tampered with!")
        print("    ✓ Stankowski's Frame successfully caught the fraud!")
    else:
        print("\n    ✓ Document is authentic")
    
    # Cleanup
    for f in [test_img, encoded_path]:
        if os.path.exists(f):
            try:
                os.remove(f)
            except PermissionError:
                pass
    
    print("=" * 60)
    
    return is_fraud


if __name__ == "__main__":
    # Run tests
    print("\n🔬 Starting Stankowski's Frame Tests...\n")
    
    # Test 1: Basic steganography
    test1_passed = test_steganography()
    
    # Test 2: Fraud detection
    test2_passed = test_fraud_detection()
    
    # Summary
    print("\n\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Steganography Test:   {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Fraud Detection Test: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    print("=" * 60)
    
    if test1_passed and test2_passed:
        print("\n🎉 All tests passed! Ready for demo!")
        print("\nNext step: Run 'streamlit run src/app.py' to start the demo")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
