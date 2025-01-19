from datetime import datetime
import os
from typing import Dict, List
import base64
from io import BytesIO
import matplotlib.pyplot as plt

class ReportGenerator:
    """Generate HTML reports with network analysis results"""
    
    def __init__(self):
        # CSS styles as a separate string
        self.css_styles = """
body{font-family:Arial,sans-serif;margin:40px;background-color:#f5f5f5}
.header{background:#2c3e50;color:white;padding:20px;border-radius:5px;box-shadow:0 2px 5px rgba(0,0,0,0.1)}
.section{margin:20px 0;padding:20px;border:1px solid #ddd;border-radius:5px;background:white;box-shadow:0 2px 5px rgba(0,0,0,0.05)}
.device{margin:10px 0;padding:15px;background:#f8f9fa;border-radius:4px}
.vulnerability{color:#dc3545;font-weight:bold}
.safe{color:#28a745;font-weight:bold}
.network-map{text-align:center;margin:20px 0}
.network-map img{max-width:100%;height:auto;border-radius:5px}
.timestamp{color:#ecf0f1;font-size:0.9em}
h2{color:#2c3e50;border-bottom:2px solid #3498db;padding-bottom:10px}
"""
        # HTML template without extra spaces
        self.report_template = (
            "<!DOCTYPE html>"
            "<html>"
            "<head>"
            "<title>Network Security Analysis Report</title>"
            "<style>{css}</style>"
            "</head>"
            "<body>"
            "<div class='header'>"
            "<h1>🛡️ Network Security Analysis Report</h1>"
            "<p class='timestamp'>Generated on: {timestamp}</p>"
            "</div>"
            "<div class='section'>"
            "<h2>📊 Network Overview</h2>"
            "<p>Total devices found: {total_devices}</p>"
            "{devices_info}"
            "</div>"
            "<div class='section'>"
            "<h2>🗺️ Network Map</h2>"
            "<div class='network-map'>"
            "<img src='data:image/png;base64,{network_map}' alt='Network Map'>"
            "</div>"
            "</div>"
            "<div class='section'>"
            "<h2>🔍 Vulnerability Analysis</h2>"
            "{vulnerability_info}"
            "</div>"
            "<div class='section'>"
            "<h2>🤖 AI Analysis</h2>"
            "{ai_analysis}"
            "</div>"
            "</body>"
            "</html>"
        )
    
    def generate_report(self, 
                       devices: List[str],
                       vulnerabilities: Dict,
                       network_map_fig: plt.Figure,
                       ai_analysis: str) -> str:
        """Generate HTML report with all analysis results"""
        
        # Convert network map to base64
        img_data = BytesIO()
        network_map_fig.savefig(img_data, format='png')
        img_data.seek(0)
        network_map_b64 = base64.b64encode(img_data.read()).decode()
        
        # Generate devices info HTML
        devices_html = []
        for device in devices:
            status_class = "vulnerability" if device in vulnerabilities else "safe"
            status_text = "Vulnerabilities Found" if device in vulnerabilities else "Safe"
            devices_html.append(
                f"<div class='device'>"
                f"<h3>Device: {device}</h3>"
                f"<p class='{status_class}'>Status: {status_text}</p>"
                f"</div>"
            )
        
        # Generate vulnerabilities info HTML
        vuln_html = []
        for device, device_vulns in vulnerabilities.items():
            vuln_html.append(f"<h3>Device: {device}</h3><ul>")
            for port, banner in device_vulns.items():
                vuln_html.append(f"<li>Port {port}: {banner}</li>")
            vuln_html.append("</ul>")
        
        # Fill template
        report = self.report_template.format(
            css=self.css_styles,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            total_devices=len(devices),
            devices_info="".join(devices_html),
            network_map=network_map_b64,
            vulnerability_info="".join(vuln_html),
            ai_analysis=ai_analysis.replace("\n", "<br>")
        )
        
        # Save report
        os.makedirs("reports", exist_ok=True)
        filename = f"reports/network_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)
            
        return filename 