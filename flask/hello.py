from flask import Flask, jsonify
from flask_restful import Api, Resource
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

app = Flask(__name__)
api = Api(app)

# pip install pycryptodome
KEY = 'KHHfD7AITN5qESmMPZgwdmgRj6AxRZE5EAJB0OnZBkY='  # base64.b64encode(b'your_32_byte_key')

def encrypt_with_key(plaintext, key):
    # Generate a random initialization vector (IV)
    iv = AES.new(key, AES.MODE_CBC).iv
    # Encrypt the plaintext with AES-256 using CBC mode
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    # Combine the IV and ciphertext for storage
    encrypted_data = iv + ciphertext
    # Encode the encrypted data in base64 format for transmission/storage
    return base64.b64encode(encrypted_data).decode('utf-8')

def decrypt_with_key(encrypted_data, key):
    # Decode the encrypted data from base64 format
    encrypted_data = base64.b64decode(encrypted_data)
    # Extract the initialization vector (IV) from the encrypted data
    iv = encrypted_data[:AES.block_size]
    # Extract the ciphertext from the encrypted data
    ciphertext = encrypted_data[AES.block_size:]
    # Decrypt the ciphertext using AES-256 and CBC mode
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode('utf-8')

class EncryptData(Resource):
    def get(self):
        data = 'Hello World'
        encrypted_data = encrypt_with_key(str(data), base64.b64decode(KEY))
        return jsonify({"encrypted": encrypted_data})

class DecryptData(Resource):
    def get(self):
        encrypted_data = 'AdE0RS+ZM4iZgzZ880GYBWBRBnsp4Yw5aS1GaRTH3so='  # Replace with the encrypted data you want to decrypt
        decrypted_data = decrypt_with_key(encrypted_data, base64.b64decode(KEY))
        return jsonify({"decrypted": decrypted_data})

api.add_resource(EncryptData, '/encrypt')
api.add_resource(DecryptData, '/decrypt')

if __name__ == '__main__':
    app.run(debug=True)