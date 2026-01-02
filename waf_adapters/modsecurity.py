import json
import aiofiles
from typing import List, Dict, Any
from pathlib import Path
from core.logger import logger
from .base import BaseWAFAdapter

class ModSecurityAdapter(BaseWAFAdapter):
    """
    Adapter for ModSecurity (v3/NGINX) using standard JSON logging.
    """
    
    async def check_health(self) -> bool:
        # For simplicity, we assume if we can read the log file path or reach management URL, it's healthy.
        # Here we just check if log file logic is configured.
        return True

    async def get_logs(self, start_time: float, end_time: float) -> List[Dict[str, Any]]:
        log_path = Path(self.config.logs.get("path", "/var/log/modsec_audit.log"))
        logs = []
        
        if not log_path.exists():
            logger.warning(f"ModSecurity log file not found at {log_path}")
            return []

        # This is a naive implementation reading the whole file. 
        # In production, this would tail or seek based on timestamp.
        try:
            async with aiofiles.open(log_path, mode='r') as f:
                async for line in f:
                    try:
                        entry = json.loads(line)
                        parsed = self.parse_log_entry(entry)
                        
                        # Filter by time window if timestamps match (converting ModSec time can be tricky, assuming simplified)
                        # For this MVP, we return all and let Analyzer filter context.
                        logs.append(parsed)
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            logger.error(f"Error reading ModSec logs: {e}")
            
        return logs

    def parse_log_entry(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        """
        ModSecurity JSON format (native) to WBT format.
        """
        transaction = entry.get("transaction", {})
        messages = transaction.get("messages", [])
        
        action = "ALLOWED"
        rule_ids = []
        
        # Check if any message indicates blocking
        for msg in messages:
            if "details" in msg:
                rule_ids.append(msg["details"].get("ruleId"))
        
        # Determine strict action from HTTP response code or details
        # In ModSec, often 403 means blocked.
        if transaction.get("response", {}).get("http_code") == 403:
            action = "BLOCKED"
            
        return {
            "timestamp": transaction.get("time_stamp"),
            "request_id": transaction.get("id"),
            "rules_triggered": rule_ids,
            "action": action,
            "client_ip": transaction.get("client_ip"),
            "uri": transaction.get("request", {}).get("uri")
        }
