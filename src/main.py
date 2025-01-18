import asyncio
from network_scanner import NetworkScanner
from vulnerability_scanner import VulnerabilityScanner
from network_visualizer import NetworkVisualizer
from ai_analyzer import AIAnalyzer

async def main():
    """Main function to run the network analysis"""
    
    print("🚀 Starting Network Security Analysis")
    print("=" * 50)
    
    # Initialize components
    scanner = NetworkScanner()
    vuln_scanner = VulnerabilityScanner()
    visualizer = NetworkVisualizer()
    ai_analyzer = AIAnalyzer()
    
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
    visualizer.create_network_map(devices, vulnerabilities)
    
    # AI Analysis
    print("\n4. Performing AI Analysis...")
    ai_analysis = await ai_analyzer.analyze_network(devices, vulnerabilities)
    
    # Print results
    print("\n📊 AI Security Analysis")
    print("=" * 50)
    print(ai_analysis)

if __name__ == "__main__":
    asyncio.run(main()) 