# TEA-ECB-and-TEA-CBC-Encryption-Decryption-Program

## Overview

This program implements the Tiny Encryption Algorithm (TEA) for encrypting and decrypting images using ECB (Electronic Codebook) and CBC (Cipher Block Chaining) modes. The images are processed in grayscale, and the encrypted and decrypted results are saved and displayed.

## Prerequisites

Before running the program, ensure you have the following installed:
- Python 3.x
- `Pillow` library for image processing
- `NumPy` library for numerical operations
- `matplotlib` library for plotting
- `termcolor` library for colored terminal output

You can install the required libraries using pip:

```sh
pip install pillow numpy matplotlib termcolor
```


## Files

The project consists of the following files:
- main.py: The main script that runs the TEA encryption/decryption program.

## Usage

Steps to Run the Program:
- Directly clone the repo from my github:
  ```sh
  git clone https://github.com/hatemhussein/TEA-ECB-and-TEA-CBC-Encryption-Decryption-Program.git
- You can manually run the program by Open PyCharm and create a new project or open an existing project.
- Add main.py Script: Add the main.py script provided above to your project.
- Run the Script: Right-click on the main.py file in the Project Explorer and select "Run 'main'".
- Follow the Prompts: The program will prompt you to enter the path of the original image, key, IV, and paths to save the encrypted and decrypted images. Follow the instructions and provide the required inputs.

## Example Inputs

- Original image path:
  ```sh
  Enter the path of the original image (.bmp): /path/to/original/image.bmp
- Key:
  ```sh
  Enter the key as four words each of 8-hexadecimal digits (32-bit in binary) separated by commas (e.g., 0x12345678,0x13245768,0x12345678,0x13245768)
- IV:
  ```sh
  Enter the IV as two words each of 8-hexadecimal digits (32-bit in binary) separated by a commas (e.g., 0x11111111,0x22222222):
- Paths to Save Encrypted and Decrypted Images:
  ```sh
  Enter the path to save the encrypted ECB image: /path/to/save/encrypted_ecb_image.bmp
  Enter the path to save the decrypted ECB image: /path/to/save/decrypted_ecb_image.bmp
  Enter the path to save the encrypted CBC image: /path/to/save/encrypted_cbc_image.bmp
  Enter the path to save the decrypted CBC image: /path/to/save/decrypted_cbc_image.bmp

## Sample Outputs

The program will process the images and display the following images:

- Original Image
- Encrypted Image (ECB)
- Decrypted Image (ECB)
- Encrypted Image (CBC)
- Decrypted Image (CBC)
  
The images will be displayed in a 3x2 grid with appropriate titles and colored text.

## Troubleshooting

If you encounter any issues:

- Ensure the paths provided for the images are correct and accessible.
- Verify that the input format for the key and IV is correct (8-hexadecimal digits separated by commas).
- Check that all required libraries are installed.

## Conclusion

This program demonstrates how to use the TEA encryption algorithm in both ECB and CBC modes to encrypt and decrypt images. It provides a user-friendly interface with clear prompts and displays the results in a visually appealing manner.

## License

This project is licensed under the MIT License.
