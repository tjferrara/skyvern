#!/usr/bin/env python3
"""
Test script to verify Railway deployment works correctly.
This script tests the basic imports and functionality.
"""

import sys
import os

def test_imports():
    """Test that all critical imports work without circular import errors."""
    try:
        print("Testing basic imports...")
        
        # Test the problematic imports that were causing circular import errors
        from skyvern.client import artifacts, browser_session, workflows
        print("✓ Client modules imported successfully")
        
        from skyvern.client.artifacts import ArtifactsClient, AsyncArtifactsClient
        print("✓ Artifacts client imported successfully")
        
        from skyvern.client.browser_session import BrowserSessionClient, AsyncBrowserSessionClient
        print("✓ Browser session client imported successfully")
        
        from skyvern.client.workflows import WorkflowsClient, AsyncWorkflowsClient
        print("✓ Workflows client imported successfully")
        
        # Test main library import
        from skyvern.library import Skyvern
        print("✓ Main Skyvern library imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def test_environment():
    """Test that environment variables are properly set."""
    print("\nTesting environment variables...")
    
    required_vars = ['PYTHONPATH', 'VIDEO_PATH', 'HAR_PATH', 'LOG_PATH', 'ARTIFACT_STORAGE_PATH']
    optional_vars = ['DATABASE_STRING', 'DATABASE_URL', 'PORT', 'BROWSER_TYPE']
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✓ {var}={value}")
        else:
            print(f"✗ {var} not set")
    
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            print(f"✓ {var}={value}")
        else:
            print(f"- {var} not set (optional)")

def main():
    """Main test function."""
    print("Railway Deployment Test")
    print("=" * 50)
    
    # Test imports
    import_success = test_imports()
    
    # Test environment
    test_environment()
    
    print("\n" + "=" * 50)
    if import_success:
        print("✓ All tests passed! Railway deployment should work.")
        sys.exit(0)
    else:
        print("✗ Some tests failed. Check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 