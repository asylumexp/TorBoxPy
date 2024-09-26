from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TorrentInfoResultFile(BaseModel):
    """Represents a file within a torrent."""
    
    id: int  # File ID
    md5: str  # MD5 hash
    hash: str  # File hash
    name: str  # File name
    size: int  # File size
    s3_path: str  # S3 path
    mime_type: str  # MIME type
    short_name: str  # Short name
    absolute_path: str  # Absolute path

class TorrentInfoResult(BaseModel):
    """Represents the result of a torrent info request."""
    
    id: int  # Torrent ID
    auth_id: str  # Auth ID
    server: int  # Server ID
    hash: str  # Torrent hash
    name: str  # Torrent name
    magnet: str  # Magnet link
    size: int  # Size of the torrent
    active: bool  # Is the torrent active
    created_at: datetime  # Creation timestamp
    updated_at: datetime  # Last updated timestamp
    download_state: str  # Current download state
    seeds: int  # Number of seeds
    peers: int  # Number of peers
    ratio: float  # Ratio of uploaded to downloaded data
    progress: float  # Download progress percentage
    download_speed: int  # Download speed in bytes
    upload_speed: int  # Upload speed in bytes
    eta: int  # Estimated time of arrival in seconds
    torrent_file: bool  # Indicates if a torrent file is available
    expires_at: Optional[datetime] = None  # Expiration timestamp
    download_present: bool  # Is the download present
    files: List[TorrentInfoResultFile]  # List of files in the torrent
    download_path: str  # Path where the torrent is downloaded
    inactive_check: int  # Check for inactivity
    availability: float  # Availability of the torrent
    download_finished: bool  # Is the download finished
    tracker: Optional[str] = None  # Tracker URL
    total_uploaded: int  # Total uploaded size
    total_downloaded: int  # Total downloaded size
    cached: bool  # Is the torrent cached
    owner: str  # Owner of the torrent
    seed_torrent: bool  # Is it a seed torrent
    allow_zipped: bool  # Allow zipped downloads
    long_term_seeding: bool  # Long-term seeding allowed
    tracker_message: Optional[str] = None  # Message from the tracker
