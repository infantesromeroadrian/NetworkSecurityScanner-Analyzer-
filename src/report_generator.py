"""Módulo para generación de reportes"""
from datetime import datetime
import os
from typing import Dict
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx

class ReportGenerator:
    """Generate HTML reports with network analysis results"""
    
    def __init__(self):
        # CSS styles as a separate string
        self.css_styles = """
body{font-family:Arial,sans-serif;margin:40px;background-color:#f5f5f5}
.header{background:#2c3e50;color:white;padding:20px;border-radius:5px}
.section{margin:20px 0;padding:20px;background:white;border-radius:5px}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:20px}
.stat-card{background:#fff;padding:15px;border-radius:5px;box-shadow:0 2px 5px rgba(0,0,0,0.1)}
.chart{margin:20px 0;text-align:center}
"""
    
    def generate_network_map(self, network_info: Dict) -> plt.Figure:
        """Genera un mapa visual de la red"""
        G = nx.Graph()
        
        # Crear nodos para cada dispositivo
        for device in network_info['devices']:
            G.add_node(device, type='device')
            
        # Agregar conexiones
        for interface, details in network_info['device_details'].items():
            G.add_edge(details['ip'], details['broadcast'])
            
        # Crear figura
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', 
                node_size=2000, font_size=8)
        
        return plt.gcf()
    
    def generate_report(self, 
                       network_info: Dict,
                       traffic_data: pd.DataFrame,
                       security_analysis: Dict) -> str:
        """Genera un reporte completo"""
        
        # Generar mapa de red
        network_map_fig = self.generate_network_map(network_info)
        
        # Convertir figura a base64
        img_data = BytesIO()
        network_map_fig.savefig(img_data, format='png')
        img_data.seek(0)
        network_map_b64 = base64.b64encode(img_data.read()).decode()
        plt.close()
        
        # Generar HTML
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Network Analysis Report</title>
            <style>{self.css_styles}</style>
        </head>
        <body>
            <div class="header">
                <h1>🛡️ Network Security Analysis Report</h1>
                <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="section">
                <h2>📊 Network Overview</h2>
                <div class="stats">
                    <div class="stat-card">
                        <h3>Devices Found</h3>
                        <p>{len(network_info['devices'])}</p>
                    </div>
                    <div class="stat-card">
                        <h3>Average Upload</h3>
                        <p>{traffic_data['upload'].mean():.2f} KB/s</p>
                    </div>
                    <div class="stat-card">
                        <h3>Average Download</h3>
                        <p>{traffic_data['download'].mean():.2f} KB/s</p>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>🗺️ Network Map</h2>
                <div class="chart">
                    <img src="data:image/png;base64,{network_map_b64}" alt="Network Map">
                </div>
            </div>
            
            <div class="section">
                <h2>⚠️ Security Alerts</h2>
                <ul>
                    {self._generate_security_alerts_html(security_analysis)}
                </ul>
            </div>
        </body>
        </html>
        """
        
        # Guardar reporte
        os.makedirs("reports", exist_ok=True)
        filename = f"reports/network_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_template)
            
        return filename
    
    def _generate_security_alerts_html(self, security_analysis: Dict) -> str:
        """Genera el HTML para las alertas de seguridad"""
        alerts = []
        
        if security_analysis['high_ports']:
            alerts.append("<li>🚨 Detected high port usage:</li><ul>")
            for alert in security_analysis['high_ports']:
                alerts.append(f"<li>{alert['process']} using port {alert['port']}</li>")
            alerts.append("</ul>")
            
        if security_analysis['unusual_ips']:
            alerts.append("<li>⚠️ Detected unusual IP connections:</li><ul>")
            for alert in security_analysis['unusual_ips']:
                alerts.append(f"<li>{alert['process']} connecting to {alert['ip']}</li>")
            alerts.append("</ul>")
            
        return "\n".join(alerts) if alerts else "<li>No security alerts detected</li>" 