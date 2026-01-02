import json
from pathlib import Path
from typing import Dict, Any, List
from core.logger import logger
from fpdf import FPDF
import datetime

REPORT_DIR = Path(__file__).parent.parent.parent / "reports"

class ReportGenerator:
    def generate_json(self, analysis_stats: Dict[str, Any]):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = REPORT_DIR / f"report_{timestamp}.json"
        
        # Ensure we have the list content before writing
        with open(filename, "w") as f:
            json.dump(analysis_stats, f, indent=4)
        logger.info(f"JSON Report generated: {filename}")
        return str(filename)

    def generate_pdf(self, analysis_stats: Dict[str, Any]):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = REPORT_DIR / f"report_{timestamp}.pdf"
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Header
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="WAF Benchmark Toolkit Report", ln=1, align="C")
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 10, txt=f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=1, align="C")
        pdf.ln(10)

        # Executive Summary
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "1. Executive Summary", ln=1)
        pdf.set_font("Arial", size=11)
        
        score = analysis_stats.get('total_score', 0)
        total_requests = analysis_stats.get('total_requests', 0)
        blocked = analysis_stats.get('blocked_requests', 0)
        passed = analysis_stats.get('passed_requests', 0) # Bypasses
        
        pdf.cell(0, 8, f"Total Score: {score}/100", ln=1)
        pdf.cell(0, 8, f"Total Traffic: {total_requests} Requests", ln=1)
        pdf.cell(0, 8, f"Blocked Attacks: {blocked}", ln=1)
        pdf.cell(0, 8, f"Successful Bypasses: {passed}", ln=1)
        pdf.cell(0, 8, f"False Positives: {analysis_stats.get('false_positives', 0)}", ln=1)
        pdf.ln(5)

        # 2. Attack Breakdown
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "2. Attack Vector Analysis", ln=1)
        pdf.set_font("Arial", size=10)
        
        # Need to reconstruct bypass details from the raw results if available
        # Currently analysis_stats might be just numbers. 
        # Ideally, we should pass the 'details' list.
        # Assuming analysis_stats has 'details' key which is a list of bypasses
        
        bypasses = analysis_stats.get('bypasses', [])
        if bypasses:
            pdf.set_text_color(200, 0, 0)
            pdf.cell(0, 8, f"CRITICAL: {len(bypasses)} WAF Bypasses Detected", ln=1)
            pdf.set_text_color(0, 0, 0)
            
            # Table Header
            pdf.set_fill_color(240, 240, 240)
            pdf.set_font("Arial", 'B', 9)
            pdf.cell(30, 8, "Vector ID", 1, 0, 'C', 1)
            pdf.cell(30, 8, "Category", 1, 0, 'C', 1)
            pdf.cell(15, 8, "Status", 1, 0, 'C', 1)
            pdf.cell(115, 8, "Payload (Truncated)", 1, 1, 'C', 1)
            
            pdf.set_font("Arial", size=8)
            for bypass in bypasses[:50]: # Limit to 50 in PDF to prevent overflow
                payload = bypass.get('payload', '')
                if len(payload) > 60:
                    payload = payload[:57] + "..."
                    
                pdf.cell(30, 6, str(bypass.get('vector_id', 'N/A')), 1)
                pdf.cell(30, 6, str(bypass.get('category', 'Unknown')), 1)
                pdf.cell(15, 6, str(bypass.get('status', '200')), 1)
                pdf.cell(115, 6, payload, 1, 1)
        else:
            pdf.set_text_color(0, 150, 0)
            pdf.cell(0, 10, "No bypasses detected. WAF blocked all test vectors.", ln=1)
            pdf.set_text_color(0, 0, 0)

        # 3. Full Stats Dump
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "3. Technical Metrics", ln=1)
        pdf.set_font("Courier", size=8)
        
        # Dump the rest of the stats as key-value pairs
        for key, value in analysis_stats.items():
            if key not in ['bypasses', 'timestamp']:
                try:
                    line = f"{key}: {value}"
                    # Simple text wrapping prevention
                    if len(line) > 90: line = line[:90] + "..."
                    pdf.cell(0, 5, line, ln=1)
                except:
                    pass
            
        pdf.output(str(filename))
        logger.info(f"PDF Report generated: {filename}")
        return str(filename)
