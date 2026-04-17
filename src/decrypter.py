import os
from cryptography.fernet import Fernet

# ==========================================
# RANSOMWARE DECRYPTER - INCIDENT RESPONSE
# Custom built for Renatoissance's Security Lab
# ==========================================

#  Keeping your original folder name so the script works!
TARGET_DIR = os.path.expanduser("~/WICHTIGE_FIRMEN_DATEN")
EXTENSION = ".locked"

print("[*] Renatoissance Incident Response Team activated.")

# 1. Load the secret key
try:
    with open("secret.key", "rb") as key_file:
        key = key_file.read()
    cipher = Fernet(key)
    print("[+] Secret Key successfully loaded! We have a chance.")
except FileNotFoundError:
    print("[!] FATAL ERROR: secret.key not found. The files are lost forever!")
    exit()

print(f"[*] Starting decryption process on: {TARGET_DIR}...\n")

# 2. Iterate through the directory and decrypt
for filename in os.listdir(TARGET_DIR):
    filepath = os.path.join(TARGET_DIR, filename)
    
    # We only look for files that have our .locked extension
    if os.path.isfile(filepath) and filename.endswith(EXTENSION):
        try:
            # Read the encrypted data
            with open(filepath, "rb") as f:
                encrypted_data = f.read()
            
            # Decrypt the data using the key
            decrypted_data = cipher.decrypt(encrypted_data)
            
            # Save the decrypted (readable) data back to the file
            with open(filepath, "wb") as f:
                f.write(decrypted_data)
            
            # Remove the .locked extension from the filename
            original_filepath = filepath[:-len(EXTENSION)]
            os.rename(filepath, original_filepath)
            
            print(f"[+] Decrypted and restored: {filename}")
            
        except Exception as e:
            print(f"[!] Error decrypting {filename}. Data might be corrupted: {e}")

# 3. Clean up (Delete the ransom note)
note_path = os.path.join(TARGET_DIR, "READ_ME_NOW.txt")
if os.path.exists(note_path):
    os.remove(note_path)
    print("\n[*] Deleted the attacker's ransom note.")

print("\n[!] OPERATION SUCCESSFUL. Welcome back to the Renatoissance. All systems green.")
