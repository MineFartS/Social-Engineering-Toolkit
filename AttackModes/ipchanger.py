#!/usr/bin/env python

"""
SocialEngineer - Social Engineering Toolkit
-------------------------------------------

Author      : Karthikeyan (https://karthithehacker.com)
GitHub      : https://github.com/karthi-the-hacker
Project     : SocialEngineer - An all-in-one CLI framework for social engineering

License     : Open-source — strictly for educational and ethical hacking purposes ONLY.

Note to Users:
--------------
🔐 This tool is intended solely for educational use, research, and authorized security testing.
🚫 Unauthorized use of this tool on networks you do not own or lack permission to test is illegal.
❗ If you use or modify this code, PLEASE GIVE PROPER CREDIT to the original author.

Warning to Code Thieves:
------------------------
❌ Removing this header or claiming this project as your own without credit is unethical and violates open-source principles.
🧠 Writing your own code earns respect. Copy-pasting without attribution does not.
✅ Be an ethical hacker. Respect developers' efforts and give credit where it’s due.
"""



from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.text import Text
from rich.table import Table
import os , time
import requests
from stem import Signal
from stem.control import Controller
import subprocess
import datetime
import threading
import queue
import sys


console = Console()

def start_tor_service():
    try:
        subprocess.run(['sudo', 'systemctl', 'start', 'tor'], check=True)
        status = subprocess.run(['systemctl', 'is-active', 'tor'], capture_output=True, text=True)
        if status.stdout.strip() == 'active':
            return True
        else:
            console.print("[bold red]❌ Tor service failed to start.[/bold red]")
            return False
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]❌ Error starting Tor service:[/bold red] {e}")
        return False

def get_sec():
    while True:
        user_input = input("\n⌛ Enter the interval in seconds (min 5, max 100): ").strip()
        if user_input.lower() == 'x':
            return "exit"
        if user_input.isdigit():
            seconds = int(user_input)
            if 5 <= seconds <= 100:
                return seconds
            else:
                console.print("[bold red]❌ Invalid input. Enter a number between 5 and 100.[/bold red]")
        else:
            console.print("[bold red]❌ Invalid input. Only numbers are allowed.[/bold red]")

def renew_tor_ip():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)

def get_tor_ip():
    proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    try:
        ip = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=10).json()['origin']
        return ip
    except Exception as e:
        return f"Error: {e}"

def input_listener(q):
    while True:
        user_input = input()
        q.put(user_input)
        if user_input.lower() == "x":
            break

def get_ip_country(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
        if response['status'] == 'success':
            return response['countryCode']
        else:
            return "N/A"
    except:
        return "N/A"

def start(t):
    ip_list = []
    q = queue.Queue()
    threading.Thread(target=input_listener, args=(q,), daemon=True).start()
    console.print("\n🔄 Starting IP changer...\n[bold red]❌ Press 'x'[/bold red] then Enter to stop and return to the main menu.\n")

    with Live(refresh_per_second=1) as live:
        while True:
            while not q.empty():
                user_input = q.get()
                if user_input.lower() == "x":
                    console.print("[bold red]Returning to Main Menu...[/bold red]")
                    return

            renew_tor_ip()
            time.sleep(int(t))

            ip = get_tor_ip()
            if "Error" in ip or not ip:
                display_text = Text("Waiting for IP...", style="bold yellow")
            else:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                country = get_ip_country(ip)
                entry = Text.assemble(
                    ("[+] ", "bold green"),
                    (f"New IP: ", "bold cyan"),
                    (f"{ip} ", "bold white"),
                    ("Country: ", "bold cyan"),
                    (f"{country} ", "bold yellow"),
                    ("Date & Time: ", "bold cyan"),
                    (f"{timestamp}", "bold magenta")
                )
                ip_list.append(entry)
                display_text = Text("\n".join(str(e) for e in ip_list), style="bold green")

            live.update(Panel(display_text, title="Tor IPs", border_style="blue"))
            time.sleep(1)
            