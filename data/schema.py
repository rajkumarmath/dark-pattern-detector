# data/schema.py
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class DarkPatternSample:
    text: str
    pattern_type: int  # 0-6 as defined
    pattern_name: str
    source_url: Optional[str]
    manipulative_phrases: List[str]
    context: str  # Where it appears (checkout, signup, etc.)