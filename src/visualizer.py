"""Módulo para visualización"""
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd

class NetworkVisualizer:
    @staticmethod
    def plot_traffic(df: pd.DataFrame):
        """Visualiza el tráfico de red"""
        plt.figure(figsize=(12, 6))
        
        plt.plot(df['timestamp'], df['upload'], 
                label='Subida (KB/s)', color='blue')
        plt.plot(df['timestamp'], df['download'], 
                label='Bajada (KB/s)', color='red')
        
        plt.title('Tráfico de Red en Tiempo Real')
        plt.xlabel('Tiempo')
        plt.ylabel('Velocidad (KB/s)')
        plt.legend()
        plt.grid(True)
        
        # Estadísticas
        print("\n📈 Estadísticas:")
        print(f"Velocidad media de subida: {df['upload'].mean():.2f} KB/s")
        print(f"Velocidad media de bajada: {df['download'].mean():.2f} KB/s")
        print(f"Pico de subida: {df['upload'].max():.2f} KB/s")
        print(f"Pico de bajada: {df['download'].max():.2f} KB/s")
        
        plt.show()
    
    @staticmethod
    def plot_connections(connections: pd.DataFrame):
        """Visualiza las conexiones"""
        if connections.empty:
            print("No hay conexiones para visualizar")
            return
            
        # Gráfico de estados de conexión
        status_counts = connections['status'].value_counts()
        
        plt.figure(figsize=(10, 6))
        status_counts.plot(kind='bar')
        plt.title('Estados de Conexiones')
        plt.xlabel('Estado')
        plt.ylabel('Cantidad')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Mostrar estadísticas
        print("\n🔌 Estadísticas de Conexiones:")
        print(f"Total conexiones: {len(connections)}")
        print("\nEstado de conexiones:")
        print(status_counts)
        
        plt.show() 