#!/usr/bin/env python3
"""
Simple test script to verify the import structure is correct.
This tests only the imports without external dependencies.
"""

import sys
import importlib.util

def test_module_structure():
    """Test that the module structure is correct."""
    print("Testing module structure...")
    
    # Test that the modules exist and have the right structure
    modules_to_test = [
        'skyvern.client.artifacts',
        'skyvern.client.browser_session', 
        'skyvern.client.workflows',
        'skyvern.client.credentials'
    ]
    
    for module_name in modules_to_test:
        try:
            spec = importlib.util.find_spec(module_name)
            if spec is None:
                print(f"✗ Module {module_name} not found")
                return False
            else:
                print(f"✓ Module {module_name} found")
        except Exception as e:
            print(f"✗ Error checking {module_name}: {e}")
            return False
    
    return True

def test_init_files():
    """Test that __init__.py files have the right content."""
    print("\nTesting __init__.py files...")
    
    init_files = {
        'skyvern/client/artifacts/__init__.py': ['ArtifactsClient', 'AsyncArtifactsClient'],
        'skyvern/client/browser_session/__init__.py': ['BrowserSessionClient', 'AsyncBrowserSessionClient'],
        'skyvern/client/workflows/__init__.py': ['WorkflowsClient', 'AsyncWorkflowsClient']
    }
    
    for file_path, expected_exports in init_files.items():
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                
            # Check if the file has proper imports
            if 'from .client import' in content:
                print(f"✓ {file_path} has proper imports")
                
                # Check if __all__ is defined
                if '__all__' in content:
                    print(f"✓ {file_path} has __all__ defined")
                    
                    # Check if expected exports are in __all__
                    all_exports_present = all(export in content for export in expected_exports)
                    if all_exports_present:
                        print(f"✓ {file_path} exports all expected classes")
                    else:
                        print(f"✗ {file_path} missing some expected exports")
                        return False
                else:
                    print(f"✗ {file_path} missing __all__ definition")
                    return False
            else:
                print(f"✗ {file_path} missing proper imports")
                return False
                
        except FileNotFoundError:
            print(f"✗ {file_path} not found")
            return False
        except Exception as e:
            print(f"✗ Error reading {file_path}: {e}")
            return False
    
    return True

def main():
    """Main test function."""
    print("Import Structure Test")
    print("=" * 40)
    
    structure_ok = test_module_structure()
    init_files_ok = test_init_files()
    
    print("\n" + "=" * 40)
    if structure_ok and init_files_ok:
        print("✓ All import structure tests passed!")
        print("The circular import issue should be resolved.")
        sys.exit(0)
    else:
        print("✗ Some tests failed.")
        sys.exit(1)

if __name__ == "__main__":
    main() 