from typing import List, Dict, Any, Tuple
from core.logger import logger

class DetectionEngine:
    def analyze(self, results: List[Dict[str, Any]], waf_logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyzes the traffic results to determine WAF effectiveness.
        """
        total_requests = len(results)
        blocked_requests = 0
        passed_requests = 0
        false_positives = 0
        false_negatives = 0
        
        bypasses = [] # Store details of successful attacks
        failures = [] # Store details of failed legit requests (False Positives)
        
        logger.info("Analyzing results...")
        
        for res in results:
            if "error" in res:
                continue
                
            status = res.get("status", 0)
            is_attack = "vector_id" in res # If it has a vector_id, it's an attack
            
            # Simple Logic: 403/406/400/50x usually means blocked
            # 200/201/301/302 usually means passed
            # This logic can be refined based on baselining
            
            blocked_codes = [400, 403, 404, 406, 500, 502, 503] # Depending on WAF config
            
            # Check if block
            is_blocked = status in blocked_codes
            
            if is_attack:
                if is_blocked:
                    blocked_requests += 1 # True Positive
                else:
                    passed_requests += 1 # False Negative (Bypass)
                    false_negatives += 1
                    bypasses.append({
                        "vector_id": res.get("vector_id"),
                        "category": res.get("category"),
                        "payload": res.get("payload"),
                        "status": status,
                        "mutation_id": res.get("mutation_id")
                    })
            else:
                # Legit Traffic
                if is_blocked:
                    blocked_requests += 1 # False Positive
                    false_positives += 1
                    failures.append({
                        "scenario": res.get("scenario"),
                        "status": status
                    })
                else:
                    passed_requests += 1 # True Negative
                    
        return {
            "total_requests": total_requests,
            "blocked_requests": blocked_requests,
            "passed_requests": passed_requests,
            "false_positives": false_positives,
            "false_negatives": false_negatives,
            "bypasses": bypasses,
            "failures": failures
        }
