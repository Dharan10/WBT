import urllib.parse
from typing import List

class PayloadMutator:
    """
    Applies obfuscation and encoding to payloads to test WAF normalization.
    """
    
    @staticmethod
    def mutate(payload: str) -> List[str]:
        """
        Returns a list of mutated variations of the payload.
        """
        mutations = [payload] # Always include original
        
        # URL Encoding
        mutations.append(urllib.parse.quote(payload))
        
        # Double URL Encoding
        mutations.append(urllib.parse.quote(urllib.parse.quote(payload)))
        
        # Case variation (Simple toggle for now)
        mutations.append(payload.swapcase())
        
        # Comment insertion (SQLi specific - purely illustrative for general engine)
        if " " in payload:
            mutations.append(payload.replace(" ", "/**/"))

        return list(set(mutations)) # Unique
