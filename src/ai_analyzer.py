from openai import OpenAI
from typing import Dict, List
import os
from dotenv import load_dotenv

class AIAnalyzer:
    """AI-powered network analysis using OpenAI"""
    
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
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