from pydantic import BaseModel
from typing import Optional, List, Union
from datetime import datetime
from uuid import UUID

class UserSettings(BaseModel):
    """Represents the settings for a user."""
    
    email_notifications: Optional[bool] = None
    web_notifications: Optional[bool] = None
    mobile_notifications: Optional[bool] = None
    rss_notifications: Optional[bool] = None
    download_speed_in_tab: Optional[bool] = None
    show_tracker_in_torrent: Optional[bool] = None
    stremio_quality: Optional[List[int]] = None
    stremio_resolution: Optional[List[int]] = None
    stremio_language: Optional[List[int]] = None
    stremio_cache: Optional[List[int]] = None
    stremio_size_lower: Optional[int] = None
    stremio_size_upper: Optional[int] = None
    google_drive_folder_id: Optional[str] = None
    onedrive_save_path: Optional[str] = None
    discord_id: Optional[Union[str, None]] = None  # Can be str or None
    discord_notifications: Optional[bool] = None
    stremio_allow_adult: Optional[bool] = None
    webdav_flatten: Optional[bool] = None
    stremio_seed_torrents: Optional[int] = None
    seed_torrents: Optional[int] = None
    allow_zipped: Optional[bool] = None
    stremio_allow_zipped: Optional[bool] = None
    onefichier_folder_id: Optional[Union[str, None]] = None  # Can be str or None
    gofile_folder_id: Optional[Union[str, None]] = None  # Can be str or None
    jdownloader_notifications: Optional[bool] = None
    webhook_notifications: Optional[bool] = None
    webhook_url: Optional[Union[str, None]] = None  # Can be str or None
    telegram_notifications: Optional[bool] = None
    telegram_id: Optional[Union[str, None]] = None  # Can be str or None
    mega_email: Optional[Union[str, None]] = None  # Can be str or None
    mega_password: Optional[Union[str, None]] = None  # Can be str or None

class User(BaseModel):
    """Represents a user in the system."""
    
    id: Optional[int] = None
    auth_id: Optional[UUID] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    plan: Optional[int] = None
    total_downloaded: Optional[int] = None
    customer: Optional[str] = None
    is_subscribed: Optional[bool] = None
    premium_expires_at: Optional[datetime] = None
    cooldown_until: Optional[datetime] = None
    email: Optional[str] = None
    user_referral: Optional[UUID] = None
    base_email: Optional[str] = None
    total_bytes_downloaded: Optional[int] = None
    total_bytes_uploaded: Optional[int] = None
    torrents_downloaded: Optional[int] = None
    web_downloads_downloaded: Optional[int] = None
    usenet_downloads_downloaded: Optional[int] = None
    additional_concurrent_slots: Optional[int] = None
    long_term_seeding: Optional[bool] = None
    long_term_storage: Optional[bool] = None
    settings: Optional[UserSettings] = None
