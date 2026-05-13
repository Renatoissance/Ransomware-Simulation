> ⚠️ **Disclaimer:** This project is a Proof of Concept (PoC) designed strictly for educational purposes and cybersecurity research. Do not execute this code on any system or network without explicit permission.

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
  <img src="img/Ransomware-Simulation2.png" alt="Directory populated with 100 text files" width="100%">
  <br><i>The target directory after successfully provisioning 100 dummy files.</i>
</p>

## Step 2: Payload Execution
Upon execution, `attacker.py` performs the following automated steps:
1. **Key Generation:** Generates a unique cryptographic key (`secret.key`) and saves it locally. In a real-world scenario, this key would be exfiltrated to an external Command and Control (C2) server.
2. **File Iteration:** Iterates through the predefined target directory.
3. **Encryption & Renaming:** Reads the binary data of each file, encrypts it using the AES-based Fernet scheme, overwrites the original data, and appends the `.locked` extension.

<p align="center">
  <img src="img/Ransomware-Simulation3.png" alt="Script encrypting files rapidly" width="100%">
  <br><i>Execution of the attacker.py script targeting the dummy directory.</i>
</p>

<p align="center">
  <img src="img/Ransomware-Simulation4.png" alt="Attack completion output" width="100%">
  <br><i>Terminal output confirming the successful encryption of all 100 files.</i>
</p>

After the script finishes, the unique decryption key is left in the working directory, simulating the asset an attacker would hold for ransom.

<p align="center">
  <img src="img/Ransomware-Simulation5.png" alt="Attacker script and generated secret key" width="100%">
</p>

## Step 3: The Aftermath
Once the encryption process concludes, the target directory is completely compromised. All original files are inaccessible, their file extensions have been altered to `.locked`, and the system drops a standard ransom note (`READ_ME_NOW.txt`) to demand payment.

<p align="center">
  <img src="img/Ransomware-Simulation6.png" alt="Directory showing locked files and ransom note" width="100%">
  <br><i>The compromised directory showing modified extensions and the dropped ransom note.</i>
</p>

Attempting to read the contents of the encrypted files reveals completely obfuscated ciphertext, verifying the success of the AES encryption layer.

<p align="center">
  <img src="img/Ransomware-Simulation8.png" alt="Encrypted ciphertext inside a locked file" width="100%">
  <br><i>Viewing the unreadable AES ciphertext of an encrypted dummy document.</i>
</p>

The ransom note instructs the user on how to theoretically recover their data.

<p align="center">
  <img src="img/Ransomware-Simulation7.png" alt="The custom ransom note" width="100%">
</p>

## Real-World EDR/AV Detection Note
It is worth noting that while working on this code in a shared host-to-VM folder, Microsoft Defender on the host operating system immediately flagged the custom script as malicious.

<p align="center">
  <img src="img/Ransomware-Simulation0.png" alt="Windows Defender catching the script as a Trojan" width="100%">
  <br><i>Microsoft Defender intercepting the custom payload via behavioral heuristics.</i>
</p>

The heuristic engine classified the script as `Trojan:Python/FileCoder.AI!MTB`, highlighting that the programmed behavior (rapid file iteration, cryptography imports, file extension modification) perfectly mirrors actual threat actor tooling.

---

# Phase 2: Incident Response & Recovery (Blue Team)

## Overview
Once the threat has been identified and the cryptographic key has been secured, the incident response (IR) phase begins. This stage focuses on data recovery and system restoration. For this PoC, a dedicated recovery tool (`decrypter.py`) was developed to reverse the encryption and restore the organization's critical data.

## Step 1: Key Acquisition
In a real-world scenario, the decryption key is either provided after a ransom payment (not recommended) or recovered through forensic analysis of the attacker's infrastructure. In our simulation, the key was located in the working directory.

<p align="center">
  <img src="img/Ransomware-Simulation9.png" alt="Viewing the secret key via terminal" width="100%">
  <br><i>Forensic acquisition of the Base64 encoded Fernet key.</i>
</p>

## Step 2: Restoration Process
The `decrypter.py` script (available in the `/src` directory) was deployed to the affected endpoint. The script performs the following operations:
1. **Key Loading:** Authenticates and loads the `secret.key`.
2. **Reverse Iteration:** Scans for all files with the `.locked` extension.
3. **Decryption:** Decrypts the binary data and overwrites the files with their original, readable content.
4. **Filename Restoration:** Removes the `.locked` suffix to return the files to their original state.

<p align="center">
  <img src="img/Ransomware-Simulation11.png" alt="Running the decrypter script" width="100%">
  <br><i>Execution of the Incident Response payload to initiate data recovery.</i>
</p>

## Step 3: Verification & Cleanup
The final stage of the IR process is verifying that the data is intact and removing any remaining artifacts left by the attacker.

<p align="center">
  <img src="img/Ransomware-Simulation10.png" alt="Successful decryption and cleanup" width="100%">
  <br><i>The decrypter confirms the restoration of files and the deletion of the ransom note.</i>
</p>

The system is now fully restored. All 100 dummy files are readable again, and the security breach has been remediated.

---

# Phase 3: Active Defense & Canary Agent Simulation (EDR/Sentinel)

## Overview
While Phase 2 focused on reactive Incident Response (IR) after the damage was done, Phase 3 introduces proactive **Active Defense**. For this, a custom background agent (`sentinel.py`) was developed to act as a localized Endpoint Detection and Response (EDR) tool. 

Instead of relying on static file signatures (which fail against custom/zero-day payloads like our `attacker.py`), the Sentinel utilizes **Behavioral Heuristics**. It monitors the filesystem in real-time via the `watchdog` library, specifically looking for the rapid creation of `.locked` extensions—a classic Indicator of Compromise (IoC) for ransomware.

## Execution & Real-Time Detection
First, the Sentinel agent is deployed to monitor the isolated target directory. It runs quietly in the background, continuously scanning for heuristic patterns.

<p align="center">
  <img src="img/Ransomware-Simulation11.png" alt="Sentinel initializing and monitoring the directory" width="100%">
  <br><i>The Sentinel agent successfully starting up and actively watching the target directory.</i>
</p>

Shortly after the defense is armed, the `attacker.py` payload is executed in a separate process. Within milliseconds of the first file modification, the Sentinel recognizes the malicious intent, isolates the path, and generates forensic log output directly to the terminal.

<p align="center">
  <img src="img/Ransomware-Simulation12.png" alt="Sentinel detecting the attack in real-time" width="100%">
  <br><i>The Active Defense system identifying the behavioral pattern and triggering critical alerts.</i>
</p>

## Key Takeaway: Detection vs. Prevention & The Race Condition
A critical observation in this simulation is that several files were still successfully encrypted before the simulated "Kill-Switch" was triggered. This perfectly illustrates a fundamental concept in cybersecurity: **The Race Condition**.

* **Mean Time to Detect (MTTD):** The Sentinel dropped the MTTD from potentially days (industry average) to milliseconds.
* **Damage Mitigation:** Because Python executes operations incredibly fast, a few "Canary" files were lost. However, identifying the attack on the first few files allows an EDR system to terminate the malicious process before it can traverse the network or encrypt critical databases. 

In a fully scaled enterprise environment, the Sentinel's alert would trigger an automated network isolation API, stopping Lateral Movement dead in its tracks.

---

# 🎓 Project Conclusion & Lessons Learned

This Proof of Concept successfully demonstrates the complete lifecycle of a modern cyber threat and its corresponding defenses:
1. **Red Team:** Weaponizing cryptography and automating file destruction.
2. **Incident Response:** Forensic key recovery and systematic data restoration.
3. **Blue Team/Defense:** Implementing heuristic behavioral monitoring to bridge the gap where traditional AV fails.

By building both the weapon and the shield, this project highlights the necessity of "Defense in Depth"—proving that robust security requires not just backups and decrypters, but proactive, behavior-based monitoring.

> **Final Reminder:** All tools developed in this repository are strictly for educational purposes and internal lab testing.
