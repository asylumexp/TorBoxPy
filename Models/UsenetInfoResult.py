from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from uuid import UUID

class UsenetInfoResultFile(BaseModel):
    """Represents a file within a Usenet download."""
    
    id: int  # File ID
    md5: str  # MD5 hash
    hash: str  # File hash
    name: str  # File name
    size: int  # File size
    s3_path: str  # S3 path
    mime_type: str  # MIME type
    short_name: str  # Short name
    absolute_path: str  # Absolute path

class UsenetInfoResult(BaseModel):
    """Represents the result of a Usenet info request."""
    
    id: int  # Usenet ID
    created_at: datetime  # Creation timestamp
    updated_at: datetime  # Last updated timestamp
    auth_id: UUID  # Auth ID (UUID type)
    name: str  # Name of the Usenet download
    hash: str  # Usenet hash
    download_state: str  # Current download state
    download_speed: int  # Download speed in bytes
    original_url: str  # Original URL
    eta: int  # Estimated time of arrival in seconds
    progress: int  # Download progress
    size: int  # Total size of the download
    download_id: str  # Unique download ID
    files: Optional[List[UsenetInfoResultFile]] = None  # List of files (optional)
    active: bool  # Is the download active
    cached: bool  # Is the download cached
    download_present: bool  # Is the download present
    download_finished: bool  # Is the download finished
