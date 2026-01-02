from pathlib import Path
from typing import Any, Dict
import yaml
from pydantic import BaseModel, HttpUrl, Field

class TargetConfig(BaseModel):
    url: str
    timeout: int = 10
    concurrency: int = 5
    evasion_level: int = Field(0, ge=0, le=2) # 0=None, 1=Basic, 2=Advanced
    headers: Dict[str, str] = {}

class WAFConfig(BaseModel):
    type: str = "modsecurity"
    log_path: str = "/var/log/modsec_audit.log"

class AppConfig:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent
        self.target: TargetConfig = self._load_target()
        self.waf: WAFConfig = self._load_waf()

    def _load_yaml(self, filename: str) -> Dict[str, Any]:
        path = self.base_dir / "configs" / filename
        if not path.exists():
            return {}
        with open(path, "r") as f:
            return yaml.safe_load(f) or {}

    def _load_target(self) -> TargetConfig:
        data = self._load_yaml("target.yaml").get("target", {})
        # Ensure url is present or default
        if "url" not in data:
            data["url"] = "http://waf_target:8080"
        return TargetConfig(**data)

    def _load_waf(self) -> WAFConfig:
        data = self._load_yaml("waf.yaml").get("waf", {})
        return WAFConfig(**data)

settings = AppConfig()
