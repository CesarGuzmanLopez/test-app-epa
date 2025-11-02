#!/usr/bin/env python3
"""
Cross-platform compatibility checker for T.E.S.T. runner.

This script verifies that all required components are available
and the T.E.S.T. runner can work on the current platform.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def check_python():
    """Check Python version."""
    print(f"✓ Python {sys.version}")
    if sys.version_info < (3, 6):
        print("✗ Python 3.6+ required")
        return False
    return True


def check_java():
    """Check Java availability."""
    java_candidates = ["java"]
    if os.name == "nt":  # Windows
        java_candidates.append("java.exe")

    for candidate in java_candidates:
        java_path = shutil.which(candidate)
        if java_path:
            try:
                result = subprocess.run(
                    [java_path, "-version"], capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0:
                    # Java prints version to stderr
                    version_info = (
                        result.stderr.split("\n")[0]
                        if result.stderr
                        else result.stdout.split("\n")[0]
                    )
                    print(f"✓ Java found: {java_path}")
                    print(f"  Version: {version_info.strip()}")
                    return java_path
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue

    print("✗ Java not found in PATH")
    print("  Please install Java and ensure it's in your PATH")
    print("  Windows: Add java.exe to PATH")
    print("  Mac/Linux: Install OpenJDK or Oracle Java")
    return None


def check_webtest_jar():
    """Check for WebTEST.jar file."""
    script_dir = Path(__file__).parent

    # Check possible locations
    locations = [
        script_dir / "WebTEST.jar",  # python/WebTEST.jar
        script_dir.parent / "WebTEST.jar",  # project_root/WebTEST.jar
        script_dir.parent / "target" / "WebTEST.jar",  # target/WebTEST.jar (Maven)
    ]

    for jar_path in locations:
        if jar_path.exists():
            print(f"✓ WebTEST.jar found: {jar_path}")
            return str(jar_path)

    print("✗ WebTEST.jar not found")
    print("  Searched locations:")
    for loc in locations:
        print(f"    {loc}")
    print("  Please copy WebTEST.jar to one of these locations")
    return None


def check_database_folder():
    """Check for Database folder (required by Java application)."""
    script_dir = Path(__file__).parent

    # Check possible locations
    locations = [
        script_dir / "Database",  # python/Database
        script_dir.parent / "Database",  # project_root/Database
        script_dir.parent
        / "src"
        / "main"
        / "java"
        / "ToxPredictor"
        / "Database",  # Java source
    ]

    for db_path in locations:
        if db_path.exists() and db_path.is_dir():
            print(f"✓ Database folder found: {db_path}")
            return str(db_path)

    print("✗ Database folder not found")
    print("  Searched locations:")
    for loc in locations:
        print(f"    {loc}")
    print("  Please copy the Database folder to one of these locations")
    return None


def check_test_modules():
    """Check that test modules can be imported."""
    try:
        from test.core import TESTRunner
        from test.io import FileWaiter
        from test.models import EndpointResult

        print("✓ T.E.S.T. modules import successfully")
        return True
    except ImportError as e:
        print(f"✗ Failed to import T.E.S.T. modules: {e}")
        return False


def check_xvfb():
    """Check xvfb availability (optional on Linux)."""
    if os.name == "posix":  # Unix/Linux
        xvfb_path = shutil.which("xvfb-run")
        if xvfb_path:
            print(f"✓ xvfb-run found: {xvfb_path} (optional for Linux)")
        else:
            print("ℹ xvfb-run not found (optional for Linux)")
            print("  Install with: sudo apt-get install xvfb (on Ubuntu/Debian)")
    else:
        print("ℹ xvfb not needed on Windows/Mac")


def main():
    """Run all compatibility checks."""
    print("T.E.S.T. Runner Cross-Platform Compatibility Check")
    print("=" * 50)

    all_good = True

    # Required checks
    if not check_python():
        all_good = False

    java_path = check_java()
    if not java_path:
        all_good = False

    jar_path = check_webtest_jar()
    if not jar_path:
        all_good = False

    db_path = check_database_folder()
    if not db_path:
        all_good = False

    if not check_test_modules():
        all_good = False

    # Optional checks
    check_xvfb()

    print("=" * 50)
    if all_good:
        print("✓ All required components found!")
        print("✓ T.E.S.T. runner should work on this platform")

        # Show quick test command
        print("\nQuick test command:")
        print(f"  python3 run_test.py --smiles 'CCO' --java '{java_path}'")

    else:
        print("✗ Some required components are missing")
        print("✗ Please install missing components before running T.E.S.T.")
        sys.exit(1)


if __name__ == "__main__":
    main()
