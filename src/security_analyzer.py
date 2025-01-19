"""Módulo para análisis de seguridad"""
import psutil
import socket
from typing import Dict, List

class SecurityAnalyzer:
    def __init__(self):
        self.suspicious_patterns = {
            'high_ports': [],
            'multiple_connections': [],
            'unusual_ips': [],
            'vulnerabilities': {},
            'ai_analysis': ''
        }
        
    def detect_suspicious_patterns(self):
        """Detecta patrones sospechosos"""
        HIGH_PORT_THRESHOLD = 50000
        MULTIPLE_CONN_THRESHOLD = 10
        
        for conn in psutil.net_connections(kind='inet'):
            try:
                if conn.raddr:
                    # Detectar puertos altos
                    if conn.raddr.port > HIGH_PORT_THRESHOLD:
                        process = psutil.Process(conn.pid)
                        self.suspicious_patterns['high_ports'].append({
                            'process': process.name(),
                            'port': conn.raddr.port,
                            'ip': conn.raddr.ip
                        })
                    
                    # Detectar IPs sospechosas
                    ip = conn.raddr.ip
                    if (ip.startswith('192.168.') or ip.startswith('10.')) and \
                       not ip.startswith('192.168.1.'):
                        process = psutil.Process(conn.pid)
                        self.suspicious_patterns['unusual_ips'].append({
                            'process': process.name(),
                            'ip': ip
                        })
            except:
                continue
                
        return self.suspicious_patterns
    
    def monitor_specific_ports(self, ports_to_monitor=[80, 443, 22, 3389]):
        """Monitorea puertos específicos"""
        port_activity = {port: [] for port in ports_to_monitor}
        
        for conn in psutil.net_connections(kind='inet'):
            try:
                if conn.raddr and conn.raddr.port in ports_to_monitor:
                    process = psutil.Process(conn.pid)
                    port_activity[conn.raddr.port].append({
                        'process': process.name(),
                        'local_addr': f"{conn.laddr.ip}:{conn.laddr.port}",
                        'remote_addr': f"{conn.raddr.ip}:{conn.raddr.port}",
                        'status': conn.status
                    })
            except:
                continue
                
        return port_activity 