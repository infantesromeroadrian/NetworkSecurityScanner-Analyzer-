import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Dict

class NetworkVisualizer:
    """Visualize network topology and generate reports"""
    
    def __init__(self):
        self.graph = nx.Graph()
        
    def create_network_map(self, devices: List[str], 
                          vulnerabilities: Dict) -> None:
        """Create and display network map"""
        plt.figure(figsize=(12, 8))
        
        # Add nodes
        for device in devices:
            self.graph.add_node(device)
            if device in vulnerabilities:
                # Red for vulnerable devices
                color = 'red'
            else:
                # Green for safe devices
                color = 'green'
                
            nx.draw_networkx_nodes(self.graph, 
                                 pos=nx.spring_layout(self.graph),
                                 nodelist=[device],
                                 node_color=color)
                                 
        plt.title("Network Security Map")
        plt.axis('off')
        plt.show() 