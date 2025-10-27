"""
Original Author : https://github.com/karthi-the-hacker
Fork Author     : https://github.com/minefarts
"""
from philh_myftp_biz.pc import cls
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def show_banner():

    cls()
    
    ascii_art = """
                                                                                                    v2.0

███████╗ ██████╗  ██████╗██╗ █████╗ ██╗         ███████╗███╗   ██╗ ██████╗ ██╗███╗   ██╗███████╗███████╗██████╗ 
██╔════╝██╔═══██╗██╔════╝██║██╔══██╗██║         ██╔════╝████╗  ██║██╔════╝ ██║████╗  ██║██╔════╝██╔════╝██╔══██╗
███████╗██║   ██║██║     ██║███████║██║         █████╗  ██╔██╗ ██║██║  ███╗██║██╔██╗ ██║█████╗  █████╗  ██████╔╝
╚════██║██║   ██║██║     ██║██╔══██║██║         ██╔══╝  ██║╚██╗██║██║   ██║██║██║╚██╗██║██╔══╝  ██╔══╝  ██╔══██╗
███████║╚██████╔╝╚██████╗██║██║  ██║███████╗    ███████╗██║ ╚████║╚██████╔╝██║██║ ╚████║███████╗███████╗██║  ██║
╚══════╝ ╚═════╝  ╚═════╝╚═╝╚═╝  ╚═╝╚══════╝    ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝╚═╝  ╚═╝                                                                                                                                                                                                                        
                                                               [bold green] Author: @karthithehacker
                                                                Website: Karthithehacker.com                                                                    
                                                     
"""
    console.print(ascii_art, style="bold cyan")
    
def show_credentials():
    
    cls()

    table = Table(
        title = "[bold magenta]Captured Credentials[/bold magenta]",
        show_header = True,
        header_style = "bold blue"
    )

    table.add_column("Username", style="bold green")
    table.add_column("Password")
    table.add_column("Date/Time")
    table.add_column("Template")
    table.add_column("Client IP")
    table.add_column("Device Info")

    creds = get_credentials_json()
    
    for c in creds:
        table.add_row(c['username'], c['password'], c['datetime'], c['template'], c['useragent'], c['ip'])
    
    show_banner()
    
    console.print(table)
    console.input("\n[bold yellow]↩️ Press Enter to go back... [/bold yellow]")

def nowifi():
    console.print("[bold red]❌ No WiFi interfaces found![/bold red]")
    exit()

def wifi_available(interfaces):
    options = "\n".join([f"{i+1}. [cyan]{iface}[/cyan]" for i, iface in enumerate(interfaces)])
    options += "\n0. [bold red]Back to Main Menu[/bold red]"
    console.print(Panel.fit(f"📡 [bold yellow]Available WiFi Interfaces:[/bold yellow]\n\n{options}", title="Choose Interface", style="bold green"))

def credentials(cred):

            console.print(Panel.fit(f"""
[bold green]Captured Credentials[/bold green]
[bold]Username:[/bold] {cred.get("username")}
[bold]Password:[/bold] {cred.get("password")}
[bold]Time    :[/bold] {cred.get("datetime")}
[bold]IP      :[/bold] {cred.get("ip")}
[bold]UserAgent:[/bold] {cred.get("useragent")}
""", title="🔐 New Login", border_style="green"))        

def wifiphish(inf,attack_mode,wifiname):
     console.print(Panel.fit(f"""
[bold]Attack Mode:[/bold] {attack_mode}
[bold]Device     :[/bold] {inf}
[bold]Wifi Name  :[/bold] {wifiname}
[bold]Stop       :[/bold] CTRL+C 
""", title="🚨 Launching Wifi Attack", border_style="red"))
     
def wifispam(interface, attack_mode, ssid_name, ssid_count):
     console.print(Panel.fit(f"""
[bold]Attack Mode:[/bold] {attack_mode}
[bold]Device     :[/bold] {interface}
[bold]Wifi Name  :[/bold] {ssid_name}
[bold]Wifi count :[/bold] {ssid_count}
[bold]Stop       :[/bold] CTRL+C 
""", title="🚨 Launching Wifi Attack", border_style="red"))
     
def show_wifi_targets(wifi_targets):
    show_banner()
    menu = ["📡 [bold yellow]Available WiFi Targets:[/bold yellow]\n"]
    
    for i, (bssid, essid, channel) in enumerate(wifi_targets, start=1):
        menu.append(f"[cyan]{i}.[/cyan] [bold white]{essid:<25}[/bold white] [dim]{bssid}[/dim]")
    
    menu.append("[bold red]0.[/bold red] Back to Main Menu")
    panel_content = "\n".join(menu)
    
    console.print(Panel.fit(panel_content, title="[bold green]Choose Target[/bold green]", style="bold green"))
