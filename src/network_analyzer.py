"""Módulo principal para análisis de red"""
from typing import Dict, List
import psutil
import pandas as pd
import netifaces
from datetime import datetime

class NetworkAnalyzer:
    def __init__(self):
        self.network_info = {}
        self.connections = []
        
    def get_network_info(self) -> Dict:
        """Obtiene información básica de la red"""
        network_info = {
            'devices': [],
            'device_details': {}
        }
        
        # Obtener interfaces de red
        interfaces = netifaces.interfaces()
        
        for interface in interfaces:
            try:
                addrs = netifaces.ifaddresses(interface)
                if netifaces.AF_INET in addrs:
                    for addr in addrs[netifaces.AF_INET]:
                        ip = addr['addr']
                        network_info['devices'].append(ip)
                        # Inicializar el diccionario de detalles para cada IP
                        network_info['device_details'][ip] = {
                            'interface': interface,
                            'ip': ip,
                            'netmask': addr.get('netmask', ''),
                            'broadcast': addr.get('broadcast', ''),
                            'type': 'unknown',
                            'confidence': 0,
                            'details': []
                        }
            except Exception as e:
                print(f"Error getting info for interface {interface}: {e}")
                
        return network_info
    
    def get_active_connections(self) -> pd.DataFrame:
        """Obtiene las conexiones activas del sistema"""
        connections = []
        
        for conn in psutil.net_connections(kind='inet'):
            try:
                connection_info = {
                    'local_ip': conn.laddr.ip,
                    'local_port': conn.laddr.port,
                    'remote_ip': conn.raddr.ip if conn.raddr else None,
                    'remote_port': conn.raddr.port if conn.raddr else None,
                    'status': conn.status,
                    'pid': conn.pid
                }
                connections.append(connection_info)
            except Exception as e:
                print(f"Error processing connection: {e}")
                
        return pd.DataFrame(connections) 