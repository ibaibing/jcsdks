"""
SDK validation module.
Checks if SDKs are properly configured with correct structure.
"""

from pathlib import Path
from .config import get_sdk_root, get_sdk_paths

# Expected directory structure for a valid SDK
EXPECTED_STRUCTURE = [
    "lib",
    "bin"
]

# Expected files in lib directory
EXPECTED_LIB_FILES = [
    "api.jar",
    "apdutool.jar",
    "jcwde.jar"
]

# Expected files in bin directory
EXPECTED_BIN_FILES = [
    "apdutool.bat",
    "converter.bat"
]

def validate_sdk(sdk_path: Path = None) -> dict:
    """
    Validate a specific SDK directory structure.
    
    Args:
        sdk_path: Path to SDK directory, if None validate all SDKs
        
    Returns:
        dict: Validation results with status and messages
    """
    if sdk_path:
        return _validate_single_sdk(sdk_path)
    
    # Validate all SDKs
    results = {
        "status": "success",
        "message": "All SDKs are properly configured.",
        "sdk_results": []
    }
    
    sdk_paths = get_sdk_paths()
    if not sdk_paths:
        return {
            "status": "error",
            "message": f"No SDKs found in JAVACARD_SDK_ROOT",
            "sdk_results": []
        }
    
    for sdk in sdk_paths:
        sdk_result = _validate_single_sdk(sdk)
        results["sdk_results"].append(sdk_result)
        
        if sdk_result["status"] != "success":
            results["status"] = "warning"
            results["message"] = "Some SDKs have issues."
    
    return results

def _validate_single_sdk(sdk_path: Path) -> dict:
    """
    Validate a single SDK directory.
    
    Args:
        sdk_path: Path to SDK directory
        
    Returns:
        dict: Validation results for the SDK
    """
    result = {
        "sdk_name": sdk_path.name,
        "status": "success",
        "issues": []
    }
    
    # Check basic directory structure
    for dir_name in EXPECTED_STRUCTURE:
        dir_path = sdk_path / dir_name
        if not dir_path.exists() or not dir_path.is_dir():
            result["issues"].append(f"Missing directory: {dir_name}")
            result["status"] = "error"
    
    # Check lib directory files
    lib_dir = sdk_path / "lib"
    if lib_dir.exists():
        found_jar_count = len(list(lib_dir.glob("*.jar")))
        if found_jar_count < 2:
            result["issues"].append(f"Too few JAR files in lib directory ({found_jar_count} found)")
            result["status"] = "warning"
    
    # Check bin directory files
    bin_dir = sdk_path / "bin"
    if bin_dir.exists():
        found_bat_count = len(list(bin_dir.glob("*.bat")))
        found_sh_count = len(list(bin_dir.glob("*.sh")))
        total_executables = found_bat_count + found_sh_count
        
        if total_executables < 2:
            result["issues"].append(f"Too few executable files in bin directory ({total_executables} found)")
            result["status"] = "warning"
    
    # Check for license file
    license_files = list(sdk_path.glob("LICENSE*")) + list(sdk_path.glob("license*"))
    if not license_files:
        result["issues"].append("Missing LICENSE file")
        result["status"] = "warning"
    
    return result

def validate_configuration() -> dict:
    """
    Validate the overall SDK configuration.
    
    Returns:
        dict: Configuration validation results
    """
    results = {
        "status": "success",
        "issues": []
    }
    
    # Check if SDK root is set
    sdk_root = get_sdk_root()
    if not sdk_root:
        results["status"] = "error"
        results["issues"].append("JAVACARD_SDK_ROOT environment variable is not set")
        return results
    
    # Check if SDK root exists
    sdk_root_path = Path(sdk_root)
    if not sdk_root_path.exists() or not sdk_root_path.is_dir():
        results["status"] = "error"
        results["issues"].append(f"SDK root directory does not exist: {sdk_root}")
        return results
    
    # Check if any SDKs are found
    sdk_paths = get_sdk_paths()
    if not sdk_paths:
        results["status"] = "warning"
        results["issues"].append(f"No SDKs found in {sdk_root}")
        return results
    
    # Validate each SDK
    for sdk_path in sdk_paths:
        sdk_result = _validate_single_sdk(sdk_path)
        if sdk_result["status"] != "success":
            results["issues"].extend([f"{sdk_result['sdk_name']}: {issue}" for issue in sdk_result['issues']])
            if sdk_result["status"] == "error":
                results["status"] = "error"
            elif results["status"] == "success":
                results["status"] = "warning"
    
    return results

def is_valid() -> bool:
    """
    Check if SDK configuration is valid.
    
    Returns:
        bool: True if SDK configuration is valid
    """
    result = validate_configuration()
    return result["status"] == "success"
