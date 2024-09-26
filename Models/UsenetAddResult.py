from pydantic import BaseModel
from typing import Optional

class UsenetAddResult(BaseModel):
    """Represents the result of adding a Usenet download."""
    
    hash: Optional[str] = None  # Usenet hash
    usenet_download_id: Optional[int] = None  # Usenet download ID
    auth_id: Optional[str] = None  # Auth ID
