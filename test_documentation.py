#!/usr/bin/env python3
"""
Test script to verify FFMPEG Python Helper documentation.
"""

import subprocess
import sys

def test_module_documentation():
    """Test that module documentation is accessible."""
    print("Testing module documentation...")
    
    # Test 1: Import module and check docstring
    import ffmpeg_python_helper
    assert ffmpeg_python_helper.__doc__ is not None, "Module should have docstring"
    print("[OK] Module has docstring")
    
    # Test 2: Check version and author
    assert hasattr(ffmpeg_python_helper, '__version__'), "Module should have __version__"
    assert hasattr(ffmpeg_python_helper, '__author__'), "Module should have __author__"
    print(f"[OK] Version: {ffmpeg_python_helper.__version__}")
    print(f"[OK] Author: {ffmpeg_python_helper.__author__}")
    
    return True

def test_class_documentation():
    """Test that FFMPEG class documentation is accessible."""
    print("\nTesting FFMPEG class documentation...")
    
    from ffmpeg_python_helper import FFMPEG
    
    # Test 1: Class docstring
    assert FFMPEG.__doc__ is not None, "FFMPEG class should have docstring"
    print("[OK] FFMPEG class has docstring")
    
    # Test 2: Constructor docstring
    assert FFMPEG.__init__.__doc__ is not None, "FFMPEG.__init__ should have docstring"
    print("[OK] FFMPEG.__init__ has docstring")
    
    # Test 3: Method docstrings
    methods_to_check = ['api', 'execute', 'reformat', 'gif', 'trim']
    for method_name in methods_to_check:
        method = getattr(FFMPEG, method_name)
        assert method.__doc__ is not None, f"FFMPEG.{method_name} should have docstring"
        print(f"[OK] FFMPEG.{method_name} has docstring")
    
    return True

def test_help_system():
    """Test that Python's help() system works."""
    print("\nTesting Python help() system...")
    
    # Test help() on module
    result = subprocess.run(
        [sys.executable, "-c", "import ffmpeg_python_helper; help(ffmpeg_python_helper)"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "help(ffmpeg_python_helper) should succeed"
    print("[OK] help(ffmpeg_python_helper) works")
    
    # Test help() on class
    result = subprocess.run(
        [sys.executable, "-c", "from ffmpeg_python_helper import FFMPEG; help(FFMPEG)"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "help(FFMPEG) should succeed"
    print("[OK] help(FFMPEG) works")
    
    # Test help() on method
    result = subprocess.run(
        [sys.executable, "-c", "from ffmpeg_python_helper import FFMPEG; help(FFMPEG.gif)"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "help(FFMPEG.gif) should succeed"
    print("[OK] help(FFMPEG.gif) works")
    
    return True

def test_documentation_files():
    """Test that documentation files exist."""
    print("\nTesting documentation files...")
    
    import os
    
    # Check README.md
    assert os.path.exists("README.md"), "README.md should exist"
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()
        assert len(content) > 0, "README.md should not be empty"
    print("[OK] README.md exists and is not empty")
    
    # Check API_REFERENCE.md
    assert os.path.exists("docs/API_REFERENCE.md"), "docs/API_REFERENCE.md should exist"
    with open("docs/API_REFERENCE.md", "r", encoding="utf-8") as f:
        content = f.read()
        assert len(content) > 0, "API_REFERENCE.md should not be empty"
    print("[OK] docs/API_REFERENCE.md exists and is not empty")
    
    # Check docs/README.md
    assert os.path.exists("docs/README.md"), "docs/README.md should exist"
    with open("docs/README.md", "r", encoding="utf-8") as f:
        content = f.read()
        assert len(content) > 0, "docs/README.md should not be empty"
    print("[OK] docs/README.md exists and is not empty")
    
    # Check scripts/generate_docs.py
    assert os.path.exists("scripts/generate_docs.py"), "scripts/generate_docs.py should exist"
    with open("scripts/generate_docs.py", "r", encoding="utf-8") as f:
        content = f.read()
        assert len(content) > 0, "generate_docs.py should not be empty"
    print("[OK] scripts/generate_docs.py exists and is not empty")
    
    return True

def main():
    """Run all documentation tests."""
    print("=" * 60)
    print("FFMPEG Python Helper Documentation Test")
    print("=" * 60)
    
    all_passed = True
    
    try:
        all_passed &= test_module_documentation()
    except Exception as e:
        print(f"[FAILED] Module documentation test failed: {e}")
        all_passed = False
    
    try:
        all_passed &= test_class_documentation()
    except Exception as e:
        print(f"[FAILED] Class documentation test failed: {e}")
        all_passed = False
    
    try:
        all_passed &= test_help_system()
    except Exception as e:
        print(f"[FAILED] Help system test failed: {e}")
        all_passed = False
    
    try:
        all_passed &= test_documentation_files()
    except Exception as e:
        print(f"[FAILED] Documentation files test failed: {e}")
        all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("[SUCCESS] All documentation tests passed!")
        return 0
    else:
        print("[FAILED] Some documentation tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())