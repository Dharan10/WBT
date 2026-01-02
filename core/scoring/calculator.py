from typing import Dict, Any

class ScoringEngine:
    def calculate_score(self, stats: Dict[str, int]) -> Dict[str, Any]:
        """
        Calculate a security score (0-100).
        """
        base_score = 100
        
        # Penalties
        # False Negative (Bypass) is critical: -10 points each
        # False Positive is bad for usability: -5 points each
        
        # The detector returns 'false_negatives' (which are bypasses)
        bypassed_count = stats.get("false_negatives", 0)
        false_positives = stats.get("false_positives", 0)
        
        penalty = (bypassed_count * 10) + (false_positives * 5)
        
        final_score = max(0, base_score - penalty)
        
        grade = "A"
        if final_score < 90: grade = "B"
        if final_score < 70: grade = "C"
        if final_score < 50: grade = "D"
        if final_score < 30: grade = "F"
        
        return {
            "total_score": final_score, # Consistent naming with orchestrator expectation
            "grade": grade,
            "details": {
                "bypass_penalty": bypassed_count * 10,
                "fp_penalty": false_positives * 5
            }
        }
