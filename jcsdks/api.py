"""
API module for jcsdks.
Provides backward compatible functions for jctool integration.
"""

import os
from pathlib import Path
from .config import get_sdk_root, get_sdk_paths

def list_sdks() -> list:
    """
    Get a list of available SDK directory names.
    
    Returns:
        list: List of available SDK directory names
    """
    sdk_paths = get_sdk_paths()
    return [sdk.name for sdk in sdk_paths]

def get_sdk_info(sdk_name: str) -> dict:
    """
    Get information about a specific SDK.
    
    Args:
        sdk_name: Name of the SDK directory
        
    Returns:
        dict: SDK information including path and files
    """
    sdk_root = get_sdk_root()
    if not sdk_root:
        return {}
    
    sdk_path = Path(sdk_root) / sdk_name
    if not sdk_path.exists() or not sdk_path.is_dir():
        return {}
    
    # Get SDK files and directories
    files = []
    dirs = []
    
    try:
        for item in sdk_path.iterdir():
            if item.is_file():
                files.append(item.name)
            else:
                dirs.append(item.name)
    except Exception:
        pass
    
    return {
        "name": sdk_name,
        "path": str(sdk_path),
        "files": files,
        "directories": dirs,
        "valid": True
    }

def get_sdk_resource(sdk_name: str, filename: str) -> str:
    """
    Get the path to a specific resource file in an SDK.
    
    Args:
        sdk_name: Name of the SDK directory
        filename: Relative path to the resource file
        
    Returns:
        str: Absolute path to the resource file if it exists
        
    Raises:
        FileNotFoundError: If the resource file is not found
    """
    sdk_root = get_sdk_root()
    if not sdk_root:
        raise FileNotFoundError(f"JAVACARD_SDK_ROOT not set")
    
    sdk_path = Path(sdk_root) / sdk_name
    resource_path = sdk_path / filename
    
    if resource_path.exists() and resource_path.is_file():
        return str(resource_path)
    
    raise FileNotFoundError(f"Resource not found: {resource_path}")

def get_available_sdks() -> list:
    """
    Get all available SDKs with detailed information.
    
    Returns:
        list: List of SDK information dictionaries
    """
    sdk_names = list_sdks()
    return [get_sdk_info(sdk_name) for sdk_name in sdk_names]

def get_sdk_path(sdk_name: str) -> str:
    """
    Get the path to an SDK directory.
    
    Args:
        sdk_name: Name of the SDK directory
        
    Returns:
        str: Absolute path to the SDK directory if it exists, empty string otherwise
    """
    sdk_root = get_sdk_root()
    if not sdk_root:
        return ""
    
    sdk_path = Path(sdk_root) / sdk_name
    if sdk_path.exists() and sdk_path.is_dir():
        return str(sdk_path)
    
    return ""
