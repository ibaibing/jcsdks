"""
jcsdks - JavaCard SDK Manager

A simple tool to help JavaCard developers configure and manage their JavaCard SDKs.
This project does NOT distribute any Oracle JavaCard SDK files.
"""

__version__ = "1.0.0"

from .config import get_sdk_root, set_sdk_root, get_sdk_paths, get_sdk_names
from .validator import validate_sdk
from .api import list_sdks, get_sdk_info, get_sdk_resource, get_available_sdks

__all__ = [
    "get_sdk_root",
    "set_sdk_root",
    "validate_sdk",
    "list_sdks",
    "get_sdk_info",
    "get_sdk_resource",
    "get_available_sdks"
]