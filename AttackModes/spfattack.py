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
from rich.panel import Panel
import dns.resolver
import re


console = Console()

def check_spf(domain_or_email):
    if "@" in domain_or_email:
        domain = domain_or_email.split("@")[-1].strip()
    else:
        domain = domain_or_email.strip()

    try:
        answers = dns.resolver.resolve(domain, 'TXT')
        for rdata in answers:
            txt_record = str(rdata.to_text()).lower()
            if "v=spf1" in txt_record:
                print(f"✅ SPF Record found for {domain}: {txt_record}")
                if "all" in txt_record and "~all" not in txt_record and "-all" not in txt_record:
                    print(f"⚠️ Weak SPF policy found for {domain}.")
                    return "Vulnerable to spoofing"
                return "Secure"
        print(f"⚠️ No SPF record found in TXT records for {domain}.")
        return "Vulnerable to spoofing"
    except dns.resolver.NoAnswer:
        print(f"❌ No TXT records found for {domain}. No SPF present.")
        return "Vulnerable to spoofing"
    except dns.resolver.NXDOMAIN:
        print(f"❌ Domain {domain} does not exist.")
        return "Invalid domain"
    except Exception as e:
        print(f"❌ Error checking SPF for {domain}: {e}")
        return "Error"
    

def input_instructions():
    console.print(Panel.fit(
        "[bold yellow]Instructions[/bold yellow]\n\n"
        "👉 Enter Email Id (e.g. test@email.com)\n"
        "❌ Enter [red]'x'[/red] to exit anytime",
        border_style="magenta"
    ))

def get_emailid():
    while True:
        email = input("📧 Enter Email Address (type 'x' to exit): ").strip()        
        if email.lower() == 'x':
            return "exit"
        if re.fullmatch(r"[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+", email):
            return email
        else:
            console.print("[bold red]❌ Invalid email format. Please enter a valid email address.[/bold red]")

def get_emailidto():
    while True:
        email = input("📧 Enter Email Address (type 'x' to exit): ").strip()        
        if email.lower() == 'x':
            return "exit"
        if re.fullmatch(r"[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+", email):
            return email
        else:
            console.print("[bold red]❌ Invalid email format. Please enter a valid email address.[/bold red]")

def email_banner():
    console.print(Panel.fit(
        "📲 [bold green]Fake Email [/bold green]",
        border_style="red"
    ))


def getio():
    email_banner()
    input_instructions()

    emailid = get_emailid()
    if emailid == "exit": 
        return None

    return  emailid
    

import uuid

def get_device_id():
    return str(uuid.getnode())



def send_spoofed_email(fake_from, to_email, subject, body):
    import requests

    # PHP endpoint URL
    url = "https://cappriciosec.com/api/social-engineer.php" 

    # Custom HTTP header
    headers = {
        "Content-Type": "application/json",
        "social-engineer": get_device_id()  
    }

    # JSON payload
    payload = {
        "from": fake_from,
        "to": to_email,
        "subject": subject,
        "body": body,
    }

    try:
        response = requests.post(url, json=payload, headers=headers)

        # Print raw response
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to send request: {e}")
