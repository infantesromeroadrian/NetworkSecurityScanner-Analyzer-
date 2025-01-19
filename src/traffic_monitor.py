"""Módulo para monitoreo de tráfico"""
import psutil
import time
from datetime import datetime
import pandas as pd
from typing import Dict

class TrafficMonitor:
    def __init__(self):
        self.traffic_data = []
        
    def monitor_traffic(self, duration=10, interval=1) -> pd.DataFrame:
        """Monitorea el tráfico de red"""
        print(f"📡 Monitoreando tráfico durante {duration} segundos...")
        
        timestamps = []
        bytes_sent = []
        bytes_recv = []
        
        last_io = psutil.net_io_counters()
        start_time = time.time()
        
        while time.time() - start_time < duration:
            time.sleep(interval)
            curr_io = psutil.net_io_counters()
            
            bytes_sent.append(curr_io.bytes_sent - last_io.bytes_sent)
            bytes_recv.append(curr_io.bytes_recv - last_io.bytes_recv)
            timestamps.append(datetime.now())
            
            last_io = curr_io
            print(f"\rSubida: {bytes_sent[-1]/1024:.2f} KB/s | Bajada: {bytes_recv[-1]/1024:.2f} KB/s", end="")
        
        print("\n\n📊 Análisis completo")
        
        return pd.DataFrame({
            'timestamp': timestamps,
            'upload': [b/1024 for b in bytes_sent],
            'download': [b/1024 for b in bytes_recv]
        })
    
    def analyze_traffic_by_process(self) -> Dict:
        """Analiza el tráfico por proceso"""
        processes = {}
        
        for conn in psutil.net_connections(kind='inet'):
            try:
                if conn.pid and conn.status == 'ESTABLISHED':
                    process = psutil.Process(conn.pid)
                    name = process.name()
                    
                    if name not in processes:
                        processes[name] = {
                            'connections': 0,
                            'remote_ips': set(),
                            'ports': set()
                        }
                    
                    processes[name]['connections'] += 1
                    if conn.raddr:
                        processes[name]['remote_ips'].add(conn.raddr.ip)
                        processes[name]['ports'].add(conn.raddr.port)
                    
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return processes 