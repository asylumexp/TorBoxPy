from pydantic import BaseModel

class AvailableUsenet(BaseModel):
    """Represents an available Usenet download."""
    
    name: str  # Usenet download name
    size: int  # Usenet download size in bytes
    hash: str  # Usenet download hash
