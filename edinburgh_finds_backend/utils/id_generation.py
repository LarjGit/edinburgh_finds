"""
Utility functions for generating IDs and slugs
"""
from uuid_utils import uuid7
import re


def generate_listing_id(entity_type: str) -> str:
    """
    Generate a time-ordered, prefixed UUID for a listing.
    
    Args:
        entity_type: Type of entity (venue, retailer, cafe, etc.)
    
    Returns:
        Prefixed UUID like "VEN-018e12345678abcd"
    
    """
    prefix_map = {
        "venue": "VEN"
    }
    
    prefix = prefix_map.get(entity_type, "LST")
    id_uuid = uuid7()
    short_uuid = str(id_uuid).replace('-', '')[:16]
    
    return f"{prefix}-{short_uuid}"


def generate_slug(name: str) -> str:
    """
    Generate a URL-friendly slug from entity name.
    
    Args:
        name: Entity name (e.g., "Manchester Tennis & Sports Club")
    
    Returns:
        Lowercase slug with hyphens (e.g., "manchester-tennis-sports-club")
    
        """
    slug = name.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)  # Remove special chars
    slug = re.sub(r'[-\s]+', '-', slug)    # Replace spaces with hyphens
    slug = slug.strip('-')                 # Remove leading/trailing hyphens
    
    return slug