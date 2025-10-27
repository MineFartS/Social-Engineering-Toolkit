"""
Original Author : https://github.com/karthi-the-hacker
Fork Author     : https://github.com/minefarts
"""
from philh_myftp_biz.pc import cls
from rich.console import Console
from rich.table import Table
from rich.prompt import IntPrompt

cls()
console = Console()

def main_menu():
    try:
        
        table = Table(
            title = "[bold green]Main Menu[/bold green]",
            show_header = True,
            header_style = "bold blue"
        )

        table.add_column("No.", style="bold cyan")
        table.add_column("Option", style="bold white")
        table.add_row("1", "🎯 Start Phishing Attack")
        table.add_row("2", "📲 OTP Bombing")
        table.add_row("3", "🎹 Keylogger")
        table.add_row("4", "📩 Email Bombing")
        table.add_row("5", "📧 Send Fake Email")
        table.add_row("6", "🕵️  IP Changer")
        table.add_row("0", "❌ Quit")
        
        console.print(table)
        
        return IntPrompt.ask("\n👉 Select an option")
    
    except EOFError:
        console.print("[red]❌ No input received! Exiting...[/red]")
        exit(1)