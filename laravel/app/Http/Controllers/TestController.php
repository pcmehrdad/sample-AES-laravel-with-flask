<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class TestController extends Controller
{
    protected $key = 'KHHfD7AITN5qESmMPZgwdmgRj6AxRZE5EAJB0OnZBkY='; // base64_encode(random_bytes(32));

    public function encrypt() {
        $data = 'Hello World';
        $encrypted = $this->encrypt_with_Key($data, base64_decode($this->key));
        return response()->json(['encrypted' => $encrypted]);
    }

    public function decrypt() {
        $encrypted = '2ABLxL5NbQr8G9sEpPNd+xkM2oWlq9BtnM+g4VOZurA=';
        $decrypted = $this->decrypt_with_Key($encrypted, base64_decode($this->key));
        return response()->json(['decrypted' => $decrypted]);
    }

    public function encrypt_with_Key($plaintext, $key) {
        // Generate a random initialization vector
        $iv = openssl_random_pseudo_bytes(openssl_cipher_iv_length('aes-256-cbc'));
        // Encrypt the plaintext with AES-256 using CBC mode
        $ciphertext = openssl_encrypt($plaintext, 'aes-256-cbc', $key, OPENSSL_RAW_DATA, $iv);
        // Combine the IV and ciphertext for storage
        $encryptedData = $iv . $ciphertext;
        // Encode the encrypted data in base64 format for transmission/storage
        return base64_encode($encryptedData);
    }

    public function decrypt_with_Key($encryptedData, $key) {
        // Decode the encrypted data from base64 format
        $encryptedData = base64_decode($encryptedData);
        // Extract the initialization vector (IV) from the encrypted data
        $ivLength = openssl_cipher_iv_length('aes-256-cbc');
        $iv = substr($encryptedData, 0, $ivLength);
        // Extract the ciphertext from the encrypted data
        $ciphertext = substr($encryptedData, $ivLength);
        // Decrypt the ciphertext using AES-256 and CBC mode
        return openssl_decrypt($ciphertext, 'aes-256-cbc', $key, OPENSSL_RAW_DATA, $iv);
    }
}
