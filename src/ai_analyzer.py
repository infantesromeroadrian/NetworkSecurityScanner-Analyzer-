from openai import OpenAI
from typing import Dict, List
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime

class AIAnalyzer:
    """AI-powered network analysis using OpenAI"""
    
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.risk_patterns = {
            'high_traffic': {
                'threshold': 1000,  # KB/s
                'risk_level': 'medium'
            },
            'unusual_ports': {
                'safe_ports': [80, 443, 22, 53, 123],
                'risk_level': 'high'
            },
            'connection_spikes': {
                'threshold': 50,  # conexiones por minuto
                'risk_level': 'high'
            }
        }
        
    async def analyze_network(self, 
                            devices: List[str], 
                            vulnerabilities: Dict) -> str:
        """Analyze network security using AI"""
        
        # Prepare the analysis prompt
        prompt = self._create_analysis_prompt(devices, vulnerabilities)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a cybersecurity expert analyzing network security."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error in AI analysis: {str(e)}"
            
    def _create_analysis_prompt(self, 
                              devices: List[str], 
                              vulnerabilities: Dict) -> str:
        """Create a detailed prompt for AI analysis"""
        prompt = "Please analyze this network security scan:\n\n"
        prompt += f"Total devices found: {len(devices)}\n"
        prompt += "\nActive devices:\n"
        
        for device in devices:
            prompt += f"- {device}\n"
            if device in vulnerabilities:
                prompt += "  Vulnerabilities:\n"
                for port, vuln in vulnerabilities[device].items():
                    prompt += f"  - Port {port}: {vuln}\n"
                    
        prompt += "\nPlease provide:\n"
        prompt += "1. Security assessment\n"
        prompt += "2. Risk level evaluation\n"
        prompt += "3. Specific recommendations\n"
        prompt += "4. Best practices to implement\n"
        
        return prompt 

    def analyze_network(self, 
                       traffic_data: pd.DataFrame, 
                       connections: pd.DataFrame,
                       security_alerts: Dict) -> str:
        """Analiza la red usando patrones predefinidos"""
        analysis = []
        risk_level = "low"
        
        # 1. Análisis de tráfico
        max_traffic = max(
            traffic_data['upload'].max(),
            traffic_data['download'].max()
        )
        if max_traffic > self.risk_patterns['high_traffic']['threshold']:
            analysis.append(
                f"⚠️ Alto tráfico detectado: {max_traffic:.2f} KB/s\n"
                f"   - Posible transferencia masiva de datos\n"
                f"   - Recomendación: Investigar la fuente del tráfico"
            )
            risk_level = "medium"
        
        # 2. Análisis de conexiones
        if not connections.empty:
            unusual_ports = connections[
                ~connections['remote_port'].isin(self.risk_patterns['unusual_ports']['safe_ports']) &
                (connections['remote_port'].notna())
            ]
            if len(unusual_ports) > 0:
                analysis.append(
                    f"🚨 Puertos inusuales detectados:\n"
                    f"   - {len(unusual_ports)} conexiones en puertos no estándar\n"
                    f"   - Puertos: {', '.join(map(str, unusual_ports['remote_port'].unique()))}\n"
                    f"   - Recomendación: Verificar legitimidad de estas conexiones"
                )
                risk_level = "high"
        
        # 3. Análisis de patrones sospechosos
        if security_alerts['high_ports'] or security_alerts['unusual_ips']:
            analysis.append(
                f"⛔ Patrones sospechosos detectados:\n"
                f"   - {len(security_alerts['high_ports'])} conexiones en puertos altos\n"
                f"   - {len(security_alerts['unusual_ips'])} IPs sospechosas\n"
                f"   - Recomendación: Revisar las alertas de seguridad"
            )
            risk_level = "high"
        
        # 4. Recomendaciones generales
        analysis.append(
            f"\n🛡️ Nivel de riesgo general: {risk_level.upper()}\n"
            f"\nRecomendaciones:\n"
            f"1. {'✅ Red estable' if risk_level == 'low' else '⚠️ Investigar anomalías'}\n"
            f"2. {'✅ Tráfico normal' if max_traffic < 1000 else '⚠️ Monitorear tráfico'}\n"
            f"3. {'✅ Puertos seguros' if len(unusual_ports) == 0 else '⚠️ Verificar puertos'}\n"
        )
        
        return "\n".join(analysis) 

    async def analyze_network_gpt(self, devices: List[str], vulnerabilities: Dict) -> str:
        """Analiza la red usando GPT"""
        prompt = self._create_analysis_prompt(devices, vulnerabilities)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": """Eres un experto en ciberseguridad analizando 
                    una red. Proporciona un análisis detallado, recomendaciones específicas y 
                    mejores prácticas. Usa emojis para hacer el análisis más visual."""},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error en análisis GPT: {str(e)}"

    def analyze_network(self, traffic_data: pd.DataFrame, 
                       connections: pd.DataFrame,
                       security_alerts: Dict) -> str:
        """Analiza la red usando patrones predefinidos"""
        # ... (código existente del análisis basado en patrones) ... 