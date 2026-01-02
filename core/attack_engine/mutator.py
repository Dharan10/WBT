import urllib.parse
from typing import List, Set
import random

class PayloadMutator:
    """
    Applies obfuscation and encoding to payloads to test WAF normalization.
    """
    
    # Common WAF bypass whitespace characters
    WHITESPACES = ["/**/", "%09", "%0a", "%0c", "%0d", "+"]
    
    def mutate(self, payload: str, level: int = 0) -> List[str]:
        """
        Returns a list of mutated variations of the payload based on evasion level.
        Level 0: No evasion (Just Original)
        Level 1: Basic (URL Encode, Case)
        Level 2: Advanced (Double Encode, Comments, Whitespace)
        """
        mutations: Set[str] = {payload}
        
        if level <= 0:
            return list(mutations)
            
        # --- Level 1: Basic Evasion ---
        # 1. URL Encoding
        mutations.add(urllib.parse.quote(payload))
        
        # 2. Case Switching (e.g. <sCrIpT>)
        mutations.add(self._random_case(payload))
        mutations.add(payload.upper())
        mutations.add(payload.lower())
        
        # 3. SQLi Comment Replacement (Simple)
        if " " in payload:
            mutations.add(payload.replace(" ", "/**/"))

        if level < 2:
            return list(mutations)

        # --- Level 2: Advanced Evasion ---
        # 4. Double URL Encoding
        mutations.add(urllib.parse.quote(urllib.parse.quote(payload)))
        
        # 5. Unicode / Overlong (Simulated for now via standard parse)
        # 6. Advanced Whitespace Injection
        if " " in payload:
            for ws in self.WHITESPACES:
                mutations.add(payload.replace(" ", ws))
                
        # 7. Null Byte Injection (Dangerous but valid test)
        mutations.add(payload + "%00")
        
        return list(mutations)

    def _random_case(self, s: str) -> str:
        return "".join(c.upper() if random.choice([True, False]) else c.lower() for c in s)
