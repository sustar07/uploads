import subprocess
import time
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.prompt import Prompt
import os
console = Console()
import json
from datetime import datetime

COMMANDS_LOG_FILE = "/home/rooster/Documents/project/commands.log"

def write_command_to_queue(command, args={}):
    
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source": "cli",  # CLI dashboard is adding the command
        "command": command,
        "args": args,
        "status": "pending"
    }

    with open(COMMANDS_LOG_FILE, "a") as log_file:
        log_file.write(json.dumps(entry) + "\n")  # Write as a single line JSON

    print(f"[+] Command '{command}' added to queue.")

# Example usage:
#write_command_to_queue("deauth", {"target": "XX:XX:XX:XX:XX:XX", "interface": "wlan1", "packets": 50})




def scan_wifi(interface="wlan1", duration=10):
    console = Console()
    output_prefix = "scan_results"
    csv_file = f"{output_prefix}-01.csv"

    # Start airodump-ng in background
    print(f"[+] Scanning for {duration} seconds on interface: {interface}")
    proc = subprocess.Popen(
        ["sudo", "airodump-ng", interface, "--output-format", "csv", "--write", output_prefix],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

    time.sleep(duration)
    proc.terminate()
    time.sleep(1)

    if not os.path.exists(csv_file):
        print("[!] CSV file not found.")
        return

    table = Table(title="Wi-Fi Scan Results")
    table.add_column("SSID", style="cyan")
    table.add_column("BSSID", style="magenta")
    table.add_column("Channel", style="green")
    table.add_column("Signal", style="red")

    with open(csv_file, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    networks_section = False
    for line in lines:
        if line.strip() == "":
            networks_section = True
            continue
        if not networks_section:
            continue
        parts = line.split(",")
        if len(parts) > 14:
            bssid = parts[0].strip()
            channel = parts[3].strip()
            signal = parts[8].strip()
            ssid = parts[13].strip()
            if ssid != "":
                table.add_row(ssid, bssid, channel, signal)

    console.print(table)
    console.print("sleeping for 15 seconds")
    time.sleep(15)


    
    # Optional cleanup
    os.remove(csv_file)

# Example usage
# scan_wifi("wlan1")




def check_ssh_status():
    result = subprocess.run("pgrep ssh", shell=True, stdout=subprocess.PIPE)
    return "[green]Running[/green]" if result.stdout else "[red]Stopped[/red]"


def show_dashboard():
    table = Table(title="📡 WRAMP CLI Dashboard")
    table.add_column("Option", justify="center", style="bold cyan")
    table.add_column("Description", justify="left")
    
    
    
    table.add_row("[1]", "Check Nearby Networks", style="bold magenta")
    table.add_row("[2]", "Deauth Attack",style="bold cyan")
    table.add_row("[3]", "Beacon Flood Attack",style="bold red")
    table.add_row("[4]", "Check SSH Status",style="bold green")
    table.add_row("[Q]", "[bold white]Quit[/bold white]")

    return table

def main():
    while True:
        console.clear()
        console.print(show_dashboard())

        try:
            choice = Prompt.ask("\n[bold green]Choose an option[/bold green]")
        except EOFError:
            console.print("[red]No input detected. Exiting...[/red]")
            continue


        if choice == "1":
            console.print("[bold cyan]Listing Nearby Network[/bold cyan]")
            scan_wifi("wlx001ea6ff9116")
        elif choice == "2":
            console.print("[bold red]Taking Input for deauth...[/bold red]")
            b={}
            p=input("enter bssid : ")
            q=input("enter interface : ")
            r=int(input("enter amount of packets to send"))
            b['bssid'] = p
            b['interface'] = q
            b['amount'] = r
            write_command_to_queue("deauth",b)
            
            
        elif choice == "3":
            console.print("[bold magenta]taking input for beacon flood[/bold magenta]")
            b={}
            p=input("enter target name : ")
            r=int(input("enter duration of packets to send : "))
            b['target'] = p
            b['duration'] = r
            write_command_to_queue("evil",b)
        elif choice == "4":
            console.print(f"[bold yellow]SSH Status:[/bold yellow] {check_ssh_status()}")
        
        elif choice.lower() == "q":
            console.print("[bold red]Exiting...[/bold red]")
            break
        else:
            console.print("[bold red]Invalid option! Try again.[/bold red]")

        time.sleep(1)

if __name__ == "__main__":
    main()

