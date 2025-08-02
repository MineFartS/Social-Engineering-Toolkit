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
from rich.table import Table
from includes import banner
from rich.prompt import IntPrompt
import os

console = Console()

def clear():
    os.system("clear")

def main_menu():
    try:
        table = Table(title="[bold green]Main Menu[/bold green]", show_header=True, header_style="bold blue")
        table.add_column("No.", style="bold cyan")
        table.add_column("Option", style="bold white")
        table.add_row("1", "🎯 Start Phishing Attack")
        table.add_row("2", "📲 OTP Bombing + 🎥 Webcam Hacking")
        table.add_row("3", "🎹 Keylogger")
        table.add_row("4", "📞 Fake IVR Call")
        table.add_row("5", "📩 Email Bombing")
        table.add_row("6", "📧 Send Fake Email")
        table.add_row("7", "🛠️  Settings / Configuration Menu")
        table.add_row("8", "⚙️  Generate Fake App (Coming Soon)")
        table.add_row("0", "❌ Quit")
        console.print(table)
        return IntPrompt.ask("\n👉 Select an option")
    except EOFError:
        console.print("[red]❌ No input received! Exiting...[/red]")
        exit(1)
