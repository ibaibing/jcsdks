#!/usr/bin/env python3
"""
Command-line interface for jcsdks.
Provides commands to validate, check, and configure JavaCard SDKs.

Supports both standalone usage (`python -m jcsdks validate`) and
sctool plugin integration (`sc sdks validate`).
"""

import sys
import argparse
from pathlib import Path
from .config import get_sdk_root, set_sdk_root, get_sdk_names
from .validator import validate_configuration


def build_parser() -> argparse.ArgumentParser:
    """Build the top-level argument parser with subcommands."""
    parser = argparse.ArgumentParser(
        prog="jcsdks",
        description="jcsdks - JavaCard SDK Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="This tool does NOT distribute any Oracle JavaCard SDKs.",
    )

    # Subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Validate command
    subparsers.add_parser("validate", help="Validate SDK configuration")

    # Info command
    subparsers.add_parser("info", help="Show SDK information")

    # Wizard command
    subparsers.add_parser("wizard", help="Interactive SDK configuration wizard")

    return parser


def main(argv=None) -> int:
    """
    Main entry point for CLI commands.

    Args:
        argv: Optional argument list. Defaults to ``sys.argv[1:]``.

    Returns:
        int: Exit code (0 for success, non-zero for errors)
    """
    if argv is None:
        argv = sys.argv[1:]

    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "validate":
        return cmd_validate()
    elif args.command == "info":
        return cmd_info()
    elif args.command == "wizard":
        return cmd_wizard()
    else:
        parser.print_help()
        return 1


def cmd_validate() -> int:
    """
    Validate SDK configuration.

    Returns:
        int: Exit code
    """
    result = validate_configuration()

    print("=== SDK Configuration Validation ===")
    print(f"Status: {result['status'].upper()}")

    if result['issues']:
        print("\nIssues found:")
        for issue in result['issues']:
            print(f"  - {issue}")
        return 1

    print(f"\n{result['message']}")
    return 0


def cmd_info() -> int:
    """
    Show SDK information.

    Returns:
        int: Exit code
    """
    sdk_root = get_sdk_root()
    sdk_names = get_sdk_names()

    print("=== SDK Information ===")
    print(f"JAVACARD_SDK_ROOT: {sdk_root or 'Not set'}")

    if sdk_names:
        print(f"\nDetected SDKs ({len(sdk_names)}):")
        for sdk in sdk_names:
            print(f"  - {sdk}")
    else:
        print("\nNo SDKs detected.")

    return 0


def cmd_wizard() -> int:
    """
    Interactive SDK configuration wizard.

    Returns:
        int: Exit code
    """
    print("=== JavaCard SDK Configuration Wizard ===")
    print("This wizard will help you configure your JavaCard SDKs.")
    print("Note: You must obtain SDKs directly from Oracle.")
    print("Download link: https://www.oracle.com/java/technologies/javacard-downloads.html")
    print()

    # Step 1: Check if SDKs are already configured
    sdk_root = get_sdk_root()
    if sdk_root:
        print(f"✓ JAVACARD_SDK_ROOT is already set to: {sdk_root}")
        confirm = input("Would you like to change it? (y/N): ").strip().lower()
        if confirm != "y":
            print("✓ Keeping current configuration.")
            return 0

    # Step 2: Get SDK root path
    while True:
        sdk_path = input("Enter path to your JavaCard SDKs directory: ").strip()
        if not sdk_path:
            print("Path cannot be empty.")
            continue

        path = Path(sdk_path)
        if not path.exists() or not path.is_dir():
            print(f"Error: Directory does not exist or is not accessible: {sdk_path}")
            continue

        # Try to set the path
        if set_sdk_root(sdk_path):
            print(f"✓ JAVACARD_SDK_ROOT set to: {sdk_path}")
            break
        else:
            print(f"Error: Failed to set SDK root path.")

    print()

    # Step 3: Validate the configuration
    print("Validating SDK configuration...")
    result = validate_configuration()

    if result['status'] == "success":
        print(f"✓ {result['message']}")
    else:
        print(f"! {result['message']}")
        if result['issues']:
            print("Issues found:")
            for issue in result['issues']:
                print(f"  - {issue}")

    print()
    print("=== Wizard Complete ===")
    print("You can now use the 'validate' command to check your configuration.")
    return 0


# ---------------------------------------------------------------------------
# sctool plugin integration
# ---------------------------------------------------------------------------

def dispatch(args) -> int:
    """
    Entry point for sctool plugin integration.

    Called by sctool's dispatch mechanism. ``args`` is the
    ``argparse.Namespace`` produced by sctool's top-level parser; the
    remaining plugin-specific arguments live in ``args.args``.
    """
    remainder = getattr(args, "args", None) or sys.argv[1:]
    return main(remainder)


def register() -> None:
    """Register this module with sctool as the 'sdks' plugin."""
    from sctool.plugin.registry import register_app

    register_app("sdks", dispatch)


if __name__ == "__main__":
    sys.exit(main())
