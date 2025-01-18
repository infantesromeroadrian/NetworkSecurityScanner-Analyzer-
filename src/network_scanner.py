import socket
import time
import datetime
from typing import List, Dict

class NetworkScanner:
    """Base scanner for network discovery and port analysis"""
    def __init__(self):
        self.devices = {}
        self.start_time = datetime.datetime.now()
        
    def get_local_ip(self) -> str:
        """Get the local IP address of the machine"""
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            return local_ip
        except Exception as e:
            print(f"Error getting local IP: {e}")
            return None
            
    def scan_network(self, ip_base: str) -> List[str]:
        """Scan the network for active devices"""
        active_devices = []
        print(f"\n🔍 Scanning network: {ip_base}.0/24")
        
        for i in range(1, 255):
            ip = f"{ip_base}.{i}"
            try:
                socket.setdefaulttimeout(1)
                socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((ip, 445))
                active_devices.append(ip)
                print(f"✅ Found device: {ip}")
            except:
                continue
                
        return active_devices 