"""
Original Author : https://github.com/karthi-the-hacker
Fork Author     : https://github.com/minefarts
"""
import shutil, subprocess, sys
from colorama import Fore, Style, init

init(autoreset=True)

def is_ngrok_installed():
    return shutil.which("ngrok") is not None

def is_ngrok_authenticated():
    try:
        result = subprocess.run(["ngrok", "config", "check"], capture_output=True, text=True)
        return "authtoken" in result.stdout.lower() or result.returncode == 0
    except Exception:
        return False

def check_ngrok():
    print(Fore.CYAN + "[*] Checking Ngrok setup..." + Style.RESET_ALL)
    
    if not is_ngrok_installed():
        print(Fore.RED + "❌ Ngrok is not installed.")
        print(Fore.YELLOW + "➡️  Please install it from: https://ngrok.com/download")
        print(Fore.YELLOW + "➡️  After installing, run: ngrok config add-authtoken <YOUR_TOKEN>")
        sys.exit(1)

    if not is_ngrok_authenticated():
        print(Fore.RED + "⚠️  Ngrok is installed but not configured with an authtoken.")
        print(Fore.YELLOW + "➡️  Run this command to set it up:")
        print(Fore.GREEN + "   ngrok config add-authtoken <YOUR_TOKEN>")
        sys.exit(1)

    print(Fore.GREEN + "✅ Ngrok is installed and configured properly!")
