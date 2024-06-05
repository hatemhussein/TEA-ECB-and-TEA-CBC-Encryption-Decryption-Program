import os
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from termcolor import colored
import time


# Defining some constants for the TEA algo
DELTA = 0x9E3779B9
ROUNDS = 32

# TEA Encryption function
def encrypt_tea(plaintext, key):
    L, R = plaintext
    sum = 0
    for _ in range(ROUNDS):
        sum = (sum + DELTA) & 0xFFFFFFFF
        L = (L + (((R << 4) + key[0]) ^ (R + sum) ^ ((R >> 5) + key[1]))) & 0xFFFFFFFF
        R = (R + (((L << 4) + key[2]) ^ (L + sum) ^ ((L >> 5) + key[3]))) & 0xFFFFFFFF
    return L, R

# TEA Decryption function
def decrypt_tea(ciphertext, key):
    L, R = ciphertext
    sum = DELTA << 5
    for _ in range(ROUNDS):
        R = (R - (((L << 4) + key[2]) ^ (L + sum) ^ ((L >> 5) + key[3]))) & 0xFFFFFFFF
        L = (L - (((R << 4) + key[0]) ^ (R + sum) ^ ((R >> 5) + key[1]))) & 0xFFFFFFFF
        sum = (sum - DELTA) & 0xFFFFFFFF
    return L, R


# Converting images to blocks
def image_to_blocks_conversion(image):
    pixel_array = np.array(image)
    image_shape = pixel_array.shape
    flattened_pixels = pixel_array.flatten()

    # Calculate the padding length required to make the length a multiple of 8
    pad_length = (-len(flattened_pixels)) % 8
    if pad_length > 0:
        flattened_pixels = np.pad(flattened_pixels, (0, pad_length), 'constant')

    # Convert the flat pixel array into blocks of 8 bytes
    pixel_blocks = [
        (int.from_bytes(flattened_pixels[i:i + 4], byteorder='big'),
         int.from_bytes(flattened_pixels[i + 4:i + 8], byteorder='big'))
        for i in range(0, len(flattened_pixels), 8)
    ]

    return pixel_blocks, image_shape

# Converting blocks to images
def blocks_to_image_conversion(blocks, image_shape):
    flattened_pixels = bytearray()
    for left_half, right_half in blocks:
        flattened_pixels.extend(left_half.to_bytes(4, byteorder='big'))
        flattened_pixels.extend(right_half.to_bytes(4, byteorder='big'))

    num_pixels = image_shape[0] * image_shape[1]
    flattened_pixels = flattened_pixels[:num_pixels]

    pixel_array = np.array(flattened_pixels, dtype=np.uint8).reshape(image_shape)

    return Image.fromarray(pixel_array)


# ECB Mode encryption
def encrypt_ecb_mode(plaintext_blocks, key):
    return [encrypt_tea(block, key) for block in plaintext_blocks]

# ECB Mode decryption
def decrypt_ecb_mode(ciphertext_blocks, key):
    return [decrypt_tea(block, key) for block in ciphertext_blocks]

# CBC Mode encryption
def encrypt_cbc_mode(plaintext_blocks, key, iv):
    ciphertext_blocks = []
    prev_cipher_block = iv
    for block in plaintext_blocks:
        block_to_encrypt = (block[0] ^ prev_cipher_block[0], block[1] ^ prev_cipher_block[1])
        encrypted_block = encrypt_tea(block_to_encrypt, key)
        ciphertext_blocks.append(encrypted_block)
        prev_cipher_block = encrypted_block
    return ciphertext_blocks

# CBC Mode decryption
def decrypt_cbc_mode(ciphertext_blocks, key, iv):
    plaintext_blocks = []
    prev_cipher_block = iv
    for block in ciphertext_blocks:
        decrypted_block = decrypt_tea(block, key)
        plaintext_block = (decrypted_block[0] ^ prev_cipher_block[0], decrypted_block[1] ^ prev_cipher_block[1])
        plaintext_blocks.append(plaintext_block)
        prev_cipher_block = block
    return plaintext_blocks

# Main Function
def main():
    print("--------------------------------------------------------------------")
    print("\033[36mWelcome to the TEA Encryption/Decryption Program!\033[0m")
    print("--------------------------------------------------------------------")
    image_input = input("\033[35mEnter the path of the original image: \033[0m").strip()

    if not os.path.isfile(image_input):
        raise FileNotFoundError(f"The file does not exist.")

    image = Image.open(image_input).convert("L")
    image_blocks, image_shape = image_to_blocks_conversion(image)

    key = get_key_from_user()
    iv = get_iv_from_user()

    encrypted_image_ecb_path = input("\033[35mEnter the path to save the encrypted ECB image: \033[0m").strip()
    decrypted_image_ecb_path = input("\033[35mEnter the path to save the decrypted ECB image: \033[0m").strip()
    encrypted_image_cbc_path = input("\033[35mEnter the path to save the encrypted CBC image: \033[0m").strip()
    decrypted_image_cbc_path = input("\033[35mEnter the path to save the decrypted CBC image: \033[0m").strip()

    print("\033[33mProcessing images, please wait...\033[0m")
    time.sleep(2)  # Simulate processing time

    process_and_save_images(image_blocks, image_shape, key, iv, encrypted_image_ecb_path, decrypted_image_ecb_path,
                            encrypted_image_cbc_path, decrypted_image_cbc_path, image)

    print("\033[32mImages have been processed and saved successfully!\033[0m")

# Helper Functions for User Input and Processing
def get_key_from_user():
    key_input = input("\033[35mEnter the key as four words each of 8-hexadecimal digits (32-bit in binary) separated by commas (Try 0x12345678,0x12345678,0x99AABBCC,0x99AABBCC): \033[0m")
    return [int(x, 16) for x in key_input.split(',')]

def get_iv_from_user():
    iv_input = input("\033[35mEnter the IV as two words each of 8-hexadecimal digits (32-bit in binary) separated by a commas (Try 0x11111111,0x22222222): \033[0m")
    return tuple(int(x, 16) for x in iv_input.split(','))

def process_and_save_images(image_blocks, image_shape, key, iv, encrypted_image_ecb_path, decrypted_image_ecb_path,
                            encrypted_image_cbc_path, decrypted_image_cbc_path, original_image):
    # ECB Mode Processing
    ciphertext_blocks_ecb = encrypt_ecb_mode(image_blocks, key)
    encrypted_image_ecb = blocks_to_image_conversion(ciphertext_blocks_ecb, image_shape)
    encrypted_image_ecb.save(encrypted_image_ecb_path)

    decrypted_blocks_ecb = decrypt_ecb_mode(ciphertext_blocks_ecb, key)
    decrypted_image_ecb = blocks_to_image_conversion(decrypted_blocks_ecb, image_shape)
    decrypted_image_ecb.save(decrypted_image_ecb_path)

    # CBC Mode Processing
    ciphertext_blocks_cbc = encrypt_cbc_mode(image_blocks, key, iv)
    encrypted_image_cbc = blocks_to_image_conversion(ciphertext_blocks_cbc, image_shape)
    encrypted_image_cbc.save(encrypted_image_cbc_path)

    decrypted_blocks_cbc = decrypt_cbc_mode(ciphertext_blocks_cbc, key, iv)
    decrypted_image_cbc = blocks_to_image_conversion(decrypted_blocks_cbc, image_shape)
    decrypted_image_cbc.save(decrypted_image_cbc_path)

    # Display Images
    print("\033[33mDisplaying images, please wait...\033[0m")
    time.sleep(2)  # Simulate display time
    display_images(original_image, encrypted_image_ecb, decrypted_image_ecb, encrypted_image_cbc, decrypted_image_cbc)

def display_images(original_image, encrypted_image_ecb, decrypted_image_ecb, encrypted_image_cbc, decrypted_image_cbc):
    plt.figure(figsize=(10, 8))

    plt.subplot(3, 2, 1)
    plt.title("Original Image", color='purple')
    plt.imshow(original_image, cmap='gray')
    plt.axis('off')

    plt.subplot(3, 2, 3)
    plt.title("Encrypted Image - ECB", color='green')
    plt.imshow(encrypted_image_ecb, cmap='gray')
    plt.axis('off')

    plt.subplot(3, 2, 4)
    plt.title("Decrypted Image - ECB", color='purple')
    plt.imshow(decrypted_image_ecb, cmap='gray')
    plt.axis('off')

    plt.subplot(3, 2, 5)
    plt.title("Encrypted Image - CBC", color='green')
    plt.imshow(encrypted_image_cbc, cmap='gray')
    plt.axis('off')

    plt.subplot(3, 2, 6)
    plt.title("Decrypted Image - CBC", color='purple')
    plt.imshow(decrypted_image_cbc, cmap='gray')
    plt.axis('off')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
