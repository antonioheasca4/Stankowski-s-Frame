"""
Stankowski's Frame - Steganography Module
LSB (Least Significant Bit) Steganography for Deutsche Bank Logo
"""

import json
import numpy as np
from PIL import Image
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import hashlib


class StankowskiEncoder:
    """Encodes encrypted data into images using LSB steganography"""
    
    def __init__(self, key: str = None):
        """
        Initialize encoder with encryption key
        
        Args:
            key: Encryption key (will be hashed to 32 bytes for AES-256)
        """
        if key is None:
            key = "Stankowski1974GrowthInStableFramework"
        
        # Hash the key to get exactly 32 bytes for AES-256
        self.key = hashlib.sha256(key.encode()).digest()
    
    def encrypt_data(self, data: dict) -> bytes:
        """
        Encrypt JSON data using AES-256
        
        Args:
            data: Dictionary to encrypt
            
        Returns:
            Encrypted bytes
        """
        json_str = json.dumps(data)
        json_bytes = json_str.encode('utf-8')
        
        cipher = AES.new(self.key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(json_bytes, AES.block_size))
        
        # Combine IV and ciphertext
        result = cipher.iv + ct_bytes
        return result
    
    def embed_data(self, image_path: str, secret_data: dict, output_path: str) -> bool:
        """
        Embed encrypted data into image using LSB steganography
        
        Args:
            image_path: Path to original image
            secret_data: Dictionary containing secret data (e.g., {"amount": "10000", "iban": "DE123..."})
            output_path: Path to save the encoded image
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Load image
            img = Image.open(image_path)
            img = img.convert('RGB')  # Ensure RGB mode
            img_array = np.array(img)
            
            # Encrypt the data
            encrypted = self.encrypt_data(secret_data)
            
            # Convert encrypted data to binary string
            binary_data = ''.join(format(byte, '08b') for byte in encrypted)
            
            # Add length header (32 bits for length)
            data_length = len(encrypted)
            length_binary = format(data_length, '032b')
            full_binary = length_binary + binary_data
            
            # Check if image has enough capacity
            max_bytes = img_array.shape[0] * img_array.shape[1] * 3 // 8
            if len(encrypted) + 4 > max_bytes:  # +4 for length header
                print(f"Error: Image too small. Need {len(encrypted) + 4} bytes, have {max_bytes} bytes")
                return False
            
            # Embed data in LSB of blue channel
            flat_img = img_array.reshape(-1)
            data_index = 0
            
            for i in range(2, len(flat_img), 3):  # Step by 3 to get only blue channel
                if data_index < len(full_binary):
                    # Modify LSB of blue channel
                    flat_img[i] = (flat_img[i] & 0xFE) | int(full_binary[data_index])
                    data_index += 1
                else:
                    break
            
            # Reshape and save
            encoded_img = flat_img.reshape(img_array.shape)
            result_img = Image.fromarray(encoded_img.astype('uint8'), 'RGB')
            result_img.save(output_path, quality=100, subsampling=0)
            
            print(f"✓ Data successfully embedded into {output_path}")
            print(f"  Embedded {len(encrypted)} bytes of encrypted data")
            return True
            
        except Exception as e:
            print(f"Error embedding data: {e}")
            return False


class StankowskiDecoder:
    """Decodes encrypted data from images using LSB steganography"""
    
    def __init__(self, key: str = None):
        """
        Initialize decoder with encryption key
        
        Args:
            key: Encryption key (must match encoder key)
        """
        if key is None:
            key = "Stankowski1974GrowthInStableFramework"
        
        self.key = hashlib.sha256(key.encode()).digest()
    
    def decrypt_data(self, encrypted_bytes: bytes) -> dict:
        """
        Decrypt AES-256 encrypted data
        
        Args:
            encrypted_bytes: Encrypted data (IV + ciphertext)
            
        Returns:
            Decrypted dictionary
        """
        iv = encrypted_bytes[:16]
        ct = encrypted_bytes[16:]
        
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(ct), AES.block_size)
        
        json_str = decrypted.decode('utf-8')
        return json.loads(json_str)
    
    def extract_data(self, image_path: str) -> dict:
        """
        Extract and decrypt hidden data from image
        
        Args:
            image_path: Path to encoded image
            
        Returns:
            Dictionary containing the hidden data, or None if extraction fails
        """
        try:
            # Load image
            img = Image.open(image_path)
            img = img.convert('RGB')
            img_array = np.array(img)
            
            # Extract LSB from blue channel
            flat_img = img_array.reshape(-1)
            binary_data = ''
            
            # First, extract the length (32 bits)
            for i in range(2, 32 * 3 + 2, 3):  # 32 bits from blue channel
                binary_data += str(flat_img[i] & 1)
            
            # Decode length
            data_length = int(binary_data, 2)
            
            if data_length <= 0 or data_length > 100000:  # Sanity check
                print(f"Invalid data length: {data_length}")
                return None
            
            # Extract the actual data
            binary_data = ''
            bits_needed = data_length * 8
            bit_count = 0
            
            for i in range(2 + 32 * 3, len(flat_img), 3):  # Skip length header
                if bit_count >= bits_needed:
                    break
                binary_data += str(flat_img[i] & 1)
                bit_count += 1
            
            # Convert binary to bytes
            encrypted_bytes = bytearray()
            for i in range(0, len(binary_data), 8):
                byte = binary_data[i:i+8]
                if len(byte) == 8:
                    encrypted_bytes.append(int(byte, 2))
            
            # Decrypt
            decrypted_data = self.decrypt_data(bytes(encrypted_bytes))
            print(f"✓ Data successfully extracted and decrypted")
            
            return decrypted_data
            
        except Exception as e:
            print(f"Error extracting data: {e}")
            return None


def create_demo_data():
    """Create sample data for demonstration"""
    authentic_data = {
        "amount": "10000",
        "currency": "EUR",
        "iban": "DE89370400440532013000",
        "date": "2025-12-06",
        "document_type": "contract",
        "secure_hash": "a7f3d9e2c1b4"
    }
    return authentic_data


if __name__ == "__main__":
    # Quick test
    print("Stankowski's Frame - Steganography Module Test")
    print("=" * 50)
    
    # This would be tested with actual logo
    sample_data = create_demo_data()
    print("Sample data to embed:")
    print(json.dumps(sample_data, indent=2))
