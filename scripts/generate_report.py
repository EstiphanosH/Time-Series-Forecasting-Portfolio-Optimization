"""
Script to generate a professional summary report from pipeline metrics.
"""

from typing import Dict, Any
import datetime

def generate_pdf_report(metrics: Dict[str, Any], file_path: str):
    """
    Generates a structured text report from the final pipeline metrics.
    
    Args:
        metrics (Dict[str, Any]): A dictionary containing all final metrics.
        file_path (str): The path to save the generated report.
    """
    with open(file_path, 'w') as f:
        f.write("GMF Investments - Portfolio Optimization Report\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Report Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        for section, data in metrics.items():
            f.write(f"--- {section} ---\n")
            if isinstance(data, dict):
                for key, value in data.items():
                    f.write(f"  {key}: {value}\n")
            else:
                f.write(f"  {data}\n")
            f.write("\n")
            
        f.write("=" * 50 + "\n")
        f.write("END OF REPORT\n")
    
    print(f"Report saved to: {file_path}")