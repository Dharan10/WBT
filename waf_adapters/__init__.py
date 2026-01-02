from .base import BaseWAFAdapter
from .modsecurity import ModSecurityAdapter
from core.config import settings

def get_waf_adapter() -> BaseWAFAdapter:
    adapter_type = settings.waf.adapter_type.lower()
    
    if adapter_type == "modsecurity":
        return ModSecurityAdapter()
    
    raise ValueError(f"Unknown WAF adapter type: {adapter_type}")
