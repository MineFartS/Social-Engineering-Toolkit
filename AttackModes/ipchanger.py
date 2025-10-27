"""
Original Author : https://github.com/karthi-the-hacker
Fork Author     : https://github.com/minefarts
"""
from philh_myftp_biz import thread
import time, subprocess, datetime, queue, requests
from stem.control import Controller
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.text import Text
from stem import Signal

console = Console()

def start_tor_service():
    try:

        subprocess.run(['sudo', 'systemctl', 'start', 'tor'], check=True)
        
        status = subprocess.run(['systemctl', 'is-active', 'tor'], capture_output=True, text=True)
        
        if status.stdout.strip() == 'active':
            return True
        
        else:
            console.print("[bold red]❌ Tor service failed to start.[/bold red]")
            return False
    
    except subprocess.CalledProcessError as e:
    
        console.print(f"[bold red]❌ Error starting Tor service:[/bold red] {e}")
    
        return False

def get_sec():
    while True:

        user_input = input("\n⌛ Enter the interval in seconds (min 5, max 100): ").strip()
        
        if user_input.lower() == 'x':
            return "exit"
        
        if user_input.isdigit():
        
            seconds = int(user_input)
        
            if 5 <= seconds <= 100:
                return seconds
        
            else:
                console.print("[bold red]❌ Invalid input. Enter a number between 5 and 100.[/bold red]")
        
        else:
            console.print("[bold red]❌ Invalid input. Only numbers are allowed.[/bold red]")

def renew_tor_ip():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)

def get_tor_ip():

    proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    
    try:
        # Return IP
        return requests.get(
            url = 'http://httpbin.org/ip',
            proxies = proxies,
            timeout = 10
        ).json()['origin']
    
    except Exception as e:
        return f"Error: {e}"

def input_listener(q):
    while True:

        user_input = input()
        
        q.put(user_input)
        
        if user_input.lower() == "x":
            break

def get_ip_country(ip):
    try:

        r = requests.get(
            url = f"http://ip-api.com/json/{ip}",
            timeout = 5
        ).json()

        if r['status'] == 'success':
            return r['countryCode']

        else:
            return "N/A"

    except:
        return "N/A"

def start(t):

    ip_list = []
    
    q = queue.Queue()
    
    thread(    
        func = input_listener,
        args = (q)
        #, daemon=True
    ).start()
    
    console.print("""
        "🔄 Starting IP changer...
        [bold red]❌ Press 'x'[/bold red] then Enter to stop and return to the main menu.
        "
    """)

    with Live(refresh_per_second=1) as live:

        while True:

            while not q.empty():

                user_input = q.get()

                if user_input.lower() == "x":

                    console.print("[bold red]Returning to Main Menu...[/bold red]")
                    return

            renew_tor_ip()
            time.sleep(int(t))
            ip = get_tor_ip()

            if "Error" in ip or not ip:
                display_text = Text("Waiting for IP...", style="bold yellow")
            
            else:
            
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
                country = get_ip_country(ip)
            
                entry = Text.assemble(
                    ("[+] ", "bold green"),
                    (f"New IP: ", "bold cyan"),
                    (f"{ip} ", "bold white"),
                    ("Country: ", "bold cyan"),
                    (f"{country} ", "bold yellow"),
                    ("Date & Time: ", "bold cyan"),
                    (f"{timestamp}", "bold magenta")
                )

                ip_list.append(entry)
                
                display_text = Text("\n".join(str(e) for e in ip_list), style="bold green")

            live.update(Panel(display_text, title="Tor IPs", border_style="blue"))
            
            time.sleep(1)
            