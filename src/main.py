from network_analyzer import NetworkAnalyzer
from traffic_monitor import TrafficMonitor
from security_analyzer import SecurityAnalyzer
from visualizer import NetworkVisualizer
from report_generator import ReportGenerator
from device_identifier import DeviceIdentifier
from ai_analyzer import AIAnalyzer
from network_scanner import NetworkScanner
from vulnerability_scanner import VulnerabilityScanner
import asyncio
import time

async def main():
    print("🚀 Iniciando análisis completo de seguridad de red...")
    print("=" * 50)
    
    # Inicializar todos los componentes
    network = NetworkAnalyzer()
    traffic = TrafficMonitor()
    security = SecurityAnalyzer()
    visualizer = NetworkVisualizer()
    reporter = ReportGenerator()
    identifier = DeviceIdentifier()
    ai = AIAnalyzer()
    scanner = NetworkScanner()
    vuln_scanner = VulnerabilityScanner()
    
    # 1. Escaneo de red
    print("\n1. Escaneando red local...")
    local_network = scanner.get_local_network()
    active_devices = await scanner.scan_network(local_network)
    print(f"Dispositivos activos encontrados: {len(active_devices)}")
    
    # 2. Análisis de red básico
    print("\n2. Obteniendo información de red...")
    network_info = network.get_network_info()
    connections = network.get_active_connections()
    
    # 3. Escaneo de vulnerabilidades
    print("\n3. Escaneando vulnerabilidades...")
    vulnerabilities = {}
    for device in active_devices:
        vuln_info = await vuln_scanner.scan_device(device)
        if vuln_info:
            vulnerabilities[device] = vuln_info
    
    # 4. Identificación de dispositivos
    print("\n4. Identificando dispositivos...")
    for device in network_info['devices']:
        services = vulnerabilities.get(device, {})
        device_info = identifier.identify_device(device, list(services.keys()), services)
        network_info['device_details'][device].update({
            'type': device_info['type'],
            'confidence': device_info['confidence'],
            'details': device_info['details']
        })
    
    # 5. Monitoreo de tráfico
    print("\n5. Monitoreando tráfico de red...")
    traffic_data = traffic.monitor_traffic(duration=30)
    process_analysis = traffic.analyze_traffic_by_process()
    
    # 6. Análisis de seguridad
    print("\n6. Realizando análisis de seguridad...")
    security_alerts = security.detect_suspicious_patterns()
    port_activity = security.monitor_specific_ports()
    
    # 7. Análisis de IA
    print("\n7. Realizando análisis de IA...")
    # Análisis basado en patrones
    pattern_analysis = ai.analyze_network(
        traffic_data,
        connections,
        security_alerts
    )
    
    # Análisis GPT
    print("\n🤖 Solicitando análisis detallado a GPT...")
    gpt_analysis = await ai.analyze_network_gpt(
        network_info['devices'],
        vulnerabilities
    )
    
    # Mostrar análisis GPT en terminal
    print("\n📊 Análisis de GPT:")
    print("=" * 50)
    print(gpt_analysis)
    print("=" * 50)
    
    # Combinar análisis
    security_alerts['ai_analysis'] = f"{pattern_analysis}\n\nAnálisis GPT:\n{gpt_analysis}"
    
    # 8. Visualización
    print("\n8. Generando visualizaciones...")
    visualizer.plot_traffic(traffic_data)
    visualizer.plot_connections(connections)
    
    # 9. Generar reporte
    print("\n9. Generando reporte HTML...")
    report_file = reporter.generate_report(
        network_info,
        traffic_data,
        security_alerts
    )
    
    print(f"\n✅ Análisis completado. Reporte guardado en: {report_file}")
    print("\nAbre el archivo HTML en tu navegador para ver el reporte completo.")

if __name__ == "__main__":
    asyncio.run(main()) 