# Phase 1: Threat Simulation & Exploitation (Red Team)

## Overview
The first phase of this Proof of Concept demonstrates how a typical ransomware payload operates on an infected endpoint. The custom Python script (`attacker.py`) utilizes the `cryptography` library (implementing Fernet, which is built on top of AES in CBC mode with a 128-bit key) to systematically render files inaccessible.

## Step 1: Environment Preparation
To safely simulate the attack without risking actual system integrity, a dedicated directory containing 100 dummy files was generated within the isolated Ubuntu Virtual Machine. 

A simple bash loop was used to rapidly provision the target directory with files containing realistic string data:

```bash
mkdir ~/WICHTIGE_FIRMEN_DATEN
cd ~/WICHTIGE_FIRMEN_DATEN
for i in {1..100}; do echo "Dies ist ein extrem wichtiges Firmendokument Nummer $i. Enthält geheime Finanzdaten." > "geheime_rechnung_$i.txt"; done
```

<p align="center">
  <img src="img/Ransomware-Simulation1.png" alt="Terminal command generating dummy files" width="100%">
</p>

<p align="center">
  <img src="img/Ransomware-Simulation2.png" alt="Directory populated with 100 text files" width="100%">
</p>

## Step 2: Payload Execution
Upon execution, `attacker.py` performs the following automated steps:
1. Generates a unique cryptographic key (`secret.key`) and saves it locally. In a real-world scenario, this key would be exfiltrated to an external Command and Control (C2) server.
2. Iterates through the predefined target directory.
3. Reads the binary data of each file, encrypts it, overwrites the original file, and appends the `.locked` extension to the filename.

<p align="center">
  <img src="img/Ransomware-Simulation3.png" alt="Script encrypting files rapidly" width="100%">
</p>

<p align="center">
  <img src="img/Ransomware-Simulation4.png" alt="Attack completion output" width="100%">
</p>

After the script finishes, the unique decryption key is left in the working directory (simulating the key the attacker holds).

<p align="center">
  <img src="img/Ransomware-Simulation5.png" alt="Attacker script and generated secret key" width="100%">
</p>

## Step 3: The Aftermath
Once the encryption process concludes, the target directory is completely compromised. All original files are inaccessible, their file extensions have been altered to `.locked`, and the system drops a standard ransom note (`READ_ME_NOW.txt`) to demand payment.

<p align="center">
  <img src="img/Ransomware-Simulation6.png" alt="Directory showing locked files and ransom note" width="100%">
</p>

Attempting to read the contents of the encrypted files reveals completely obfuscated ciphertext, verifying the success of the AES encryption layer.

<p align="center">
  <img src="img/Ransomware-Simulation8.png" alt="Encrypted ciphertext inside a locked file" width="100%">
</p>

The ransom note instructs the user on how to theoretically recover their data.

<p align="center">
  <img src="img/Ransomware-Simulation7.png" alt="The custom ransom note" width="100%">
</p>

## Real-World EDR/AV Detection Note
It is worth noting that while working on this code in a shared host-to-VM folder, Microsoft Defender on the host operating system immediately flagged the custom script as malicious.

<p align="center">
  <img src="img/Ransomware-Simulation0.png" alt="Windows Defender catching the script as a Trojan" width="100%">
</p>

The heuristic engine classified the script as `Trojan:Python/FileCoder.AI!MTB`, highlighting that the programmed behavior (rapid file iteration, cryptography imports, file extension modification) perfectly mirrors actual threat actor tooling.

TO BE CONTINUED...
