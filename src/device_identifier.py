"""Módulo para identificación de dispositivos"""
from typing import Dict, List
import socket
import re

class DeviceIdentifier:
    def __init__(self):
        self.device_signatures = {
            'printer': [
                r'printer',
                r'hp',
                r'epson',
                r'canon',
                r'brother'
            ],
            'router': [
                r'router',
                r'gateway',
                r'modem',
                r'huawei',
                r'tp-link',
                r'cisco'
            ],
            'mobile': [
                r'android',
                r'iphone',
                r'mobile',
                r'samsung',
                r'huawei'
            ],
            'iot': [
                r'camera',
                r'thermostat',
                r'smart.*bulb',
                r'alexa',
                r'nest'
            ]
        }
    
    def identify_device(self, ip: str, open_ports: List[int], services: Dict) -> Dict:
        """Identifica el tipo de dispositivo basado en sus características"""
        device_info = {
            'type': 'unknown',
            'confidence': 0,
            'details': []
        }
        
        try:
            # Intentar obtener el hostname
            hostname = socket.gethostbyaddr(ip)[0].lower()
        except:
            hostname = ''
        
        # Analizar puertos y servicios
        for device_type, signatures in self.device_signatures.items():
            confidence = 0
            details = []
            
            # Verificar hostname
            for signature in signatures:
                if re.search(signature, hostname, re.I):
                    confidence += 30
                    details.append(f"Hostname matches {device_type} pattern")
            
            # Verificar servicios
            for port, service in services.items():
                service_str = str(service).lower()
                for signature in signatures:
                    if re.search(signature, service_str, re.I):
                        confidence += 20
                        details.append(f"Service on port {port} matches {device_type}")
            
            # Verificar puertos comunes
            if device_type == 'printer' and 9100 in open_ports:
                confidence += 25
                details.append("Found printer port (9100)")
            elif device_type == 'router' and 80 in open_ports:
                confidence += 15
                details.append("Found web interface port (80)")
            
            # Actualizar si encontramos mejor coincidencia
            if confidence > device_info['confidence']:
                device_info = {
                    'type': device_type,
                    'confidence': confidence,
                    'details': details
                }
        
        return device_info 