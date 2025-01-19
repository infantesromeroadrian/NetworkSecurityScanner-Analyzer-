import asyncio
from network_scanner import NetworkScanner
from vulnerability_scanner import VulnerabilityScanner
from network_visualizer import NetworkVisualizer
from ai_analyzer import AIAnalyzer
from report_generator import ReportGenerator
import matplotlib.pyplot as plt

async def main():
    """Main function to run the network analysis"""
    
    print("🚀 Starting Network Security Analysis")
    print("=" * 50)
    
    # Initialize components
    scanner = NetworkScanner()
    vuln_scanner = VulnerabilityScanner()
    visualizer = NetworkVisualizer()
    ai_analyzer = AIAnalyzer()
    report_gen = ReportGenerator()
    
    # Get local network information
    local_ip = scanner.get_local_ip()
    ip_base = '.'.join(local_ip.split('.')[:-1])
    
    # Scan network
    print("\n1. Scanning Network...")
    devices = scanner.scan_network(ip_base)
    
    # Scan for vulnerabilities
    print("\n2. Checking Vulnerabilities...")
    vulnerabilities = {}
    for device in devices:
        vulnerabilities[device] = vuln_scanner.scan_ports(device)
    
    # Visualize network
    print("\n3. Generating Network Map...")
    fig = plt.figure(figsize=(12, 8))
    visualizer.create_network_map(devices, vulnerabilities)
    
    # AI Analysis
    print("\n4. Performing AI Analysis...")
    ai_analysis = await ai_analyzer.analyze_network(devices, vulnerabilities)
    
    # Generate Report
    print("\n5. Generating HTML Report...")
    report_file = report_gen.generate_report(
        devices,
        vulnerabilities,
        fig,
        ai_analysis
    )
    
    print(f"\n✅ Report generated: {report_file}")
    print("\nOpen the HTML file in your browser to view the complete report.")

if __name__ == "__main__":
    asyncio.run(main()) 