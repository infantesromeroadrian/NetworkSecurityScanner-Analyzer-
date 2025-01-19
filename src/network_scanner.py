"""Módulo para escanear la red local"""
import socket
import asyncio
import ipaddress
from typing import List
import netifaces

class NetworkScanner:
    def __init__(self):
        self.timeout = 1  # timeout en segundos
        
    def get_local_network(self) -> str:
        """Obtiene la dirección de red local"""
        try:
            # Obtener la interfaz predeterminada
            gateways = netifaces.gateways()
            default_gateway = gateways['default'][netifaces.AF_INET][0]
            
            # Obtener la dirección IP local
            for interface in netifaces.interfaces():
                addrs = netifaces.ifaddresses(interface)
                if netifaces.AF_INET in addrs:
                    for addr in addrs[netifaces.AF_INET]:
                        ip = addr['addr']
                        if ip != '127.0.0.1':  # Ignorar localhost
                            # Devolver la red en formato CIDR
                            return f"{ip.rsplit('.', 1)[0]}.0/24"
                            
        except Exception as e:
            print(f"Error obteniendo red local: {e}")
            return "192.168.1.0/24"  # Red por defecto
            
    async def scan_port(self, ip: str, port: int) -> bool:
        """Escanea un puerto específico"""
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(ip, port),
                timeout=self.timeout
            )
            writer.close()
            await writer.wait_closed()
            return True
        except:
            return False
            
    async def scan_host(self, ip: str) -> bool:
        """Verifica si un host está activo"""
        # Puertos comunes para escanear
        common_ports = [80, 443, 22, 445]
        
        try:
            # Intentar primero con socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((ip, 445))  # Puerto SMB común en Windows
            sock.close()
            
            if result == 0:
                return True
                
            # Si no responde al primer intento, probar puertos comunes
            tasks = [self.scan_port(ip, port) for port in common_ports]
            results = await asyncio.gather(*tasks)
            return any(results)
            
        except Exception:
            return False
            
    async def scan_network(self, network: str) -> List[str]:
        """Escanea toda la red en busca de dispositivos activos"""
        active_devices = []
        network_addr = ipaddress.ip_network(network)
        
        print(f"Escaneando red {network}...")
        tasks = []
        
        for ip in network_addr.hosts():
            ip_str = str(ip)
            tasks.append(self.scan_host(ip_str))
            
        # Ejecutar escaneos en paralelo
        results = await asyncio.gather(*tasks)
        
        # Recopilar resultados
        for ip, is_active in zip(network_addr.hosts(), results):
            if is_active:
                active_devices.append(str(ip))
                print(f"Dispositivo encontrado: {ip}")
                
        return active_devices 