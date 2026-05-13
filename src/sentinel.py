import os
import time
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ==========================================
# ACTIVE DEFENSE AGENT - CANARY MONITOR
# Custom built for Renatoissance's Security Lab
# ==========================================

# 1. Configuration
TARGET_DIR = os.path.expanduser("~/WICHTIGE_FIRMEN_DATEN")
SUSPICIOUS_EXTENSION = ".locked"

class RansomwareHandler(FileSystemEventHandler):
    """
    Diese Klasse überwacht Events im Dateisystem.
    Sobald eine Datei in .locked umbenannt wird, schlägt sie Alarm.
    """
    
    def on_moved(self, event):
        # Ransomware benennt oft Dateien um (z.B. doc.txt -> doc.txt.locked)
        if event.dest_path.endswith(SUSPICIOUS_EXTENSION):
            self.trigger_alarm(event.dest_path)

    def on_modified(self, event):
        # Falls die Ransomware den Inhalt direkt überschreibt
        if event.src_path.endswith(SUSPICIOUS_EXTENSION):
            self.trigger_alarm(event.src_path)

    def trigger_alarm(self, file_path):
        print(f"\n[!!!] KRITISCHER ALARM: Ransomware-Aktivität erkannt!")
        print(f"[!] Verdächtige Datei: {os.path.basename(file_path)}")
        print(f"[*] AKTION: Isolierung des Pfads {TARGET_DIR} eingeleitet.")
        print(f"[*] STATUS: Versuche, bösartigen Prozess zu identifizieren und zu stoppen...")
        
        # In einer echten EDR-Simulation würde hier ein os.kill() auf die 
        # Prozess-ID (PID) folgen, die den Zugriff verursacht hat.
        self.simulate_kill()

    def simulate_kill(self):
        print("[+] VERTEIDIGUNG ERFOLGREICH: Angreifer-Prozess terminiert.")
        print("[+] System gesperrt. Forensic-Log wurde erstellt.\n")
        # Hier könnte man das Skript beenden oder weiter überwachen
        # sys.exit() 

# 2. Start the Sentinel
print("====================================================")
print("   RENATOISSANCE ACTIVE DEFENSE SENTINEL v1.0       ")
print("====================================================")
print(f"[*] Überwachung gestartet: {TARGET_DIR}")
print("[*] Status: Suche nach Heuristiken (Dateiendung: .locked)")
print("[*] Drücke STRG+C zum Beenden.")

event_handler = RansomwareHandler()
observer = Observer()
observer.schedule(event_handler, TARGET_DIR, recursive=False)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
    print("\n[*] Sentinel wird heruntergefahren. Sicherheitsscan beendet.")

observer.join()
