"""
Configuration management for jcsdks.
Handles SDK root path configuration and environment variables.
"""

import os
from pathlib import Path

# Environment variable name for SDK root
SDK_ROOT_ENV = "JAVACARD_SDK_ROOT"

def get_sdk_root() -> str:
    """
    Get the SDK root path from environment variable.
    
    Returns:
        str: SDK root path if set, empty string otherwise
    """
    return os.environ.get(SDK_ROOT_ENV, "")

def set_sdk_root(path: str) -> bool:
    """
    Set the SDK root path in environment variable.
    
    Args:
        path: Path to SDK root directory
        
    Returns:
        bool: True if path is valid and set successfully
    """
    try:
        sdk_path = Path(path)
        if not sdk_path.exists() or not sdk_path.is_dir():
            return False
        
        os.environ[SDK_ROOT_ENV] = str(sdk_path)
        return True
    except Exception:
        return False

def get_sdk_paths() -> list:
    """
    Get paths to all detected SDKs.
    
    Returns:
        list: List of Path objects to SDK directories
    """
    import re
    sdk_root = get_sdk_root()
    if not sdk_root:
        return []
    
    sdk_root_path = Path(sdk_root)
    sdk_paths = []
    
    try:
        # Look for directories matching jcXXX_kit pattern (starts with jc followed by a digit)
        for item in sdk_root_path.iterdir():
            if item.is_dir() and re.match(r'^jc\d.*_kit$', item.name, re.IGNORECASE):
                sdk_paths.append(item)
        return sdk_paths
    except Exception:
        return []

def get_sdk_names() -> list:
    """
    Get names of all detected SDKs.
    
    Returns:
        list: List of SDK directory names
    """
    return [sdk.name for sdk in get_sdk_paths()]
