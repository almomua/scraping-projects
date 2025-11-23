"""
Publication Verification Script
================================
Run this script before publishing to GitHub to verify everything is ready.
"""

import os
import re
import sys

def check_api_keys():
    """Check for hardcoded API keys in Python files"""
    print("\n[*] Checking for hardcoded API keys...")
    
    api_key_patterns = [
        r'AIzaSy[A-Za-z0-9_-]{33}',  # Google API keys
        r'sk-[A-Za-z0-9]{48}',        # OpenAI keys
        r'gsk_[A-Za-z0-9]{52}',       # Groq keys
    ]
    
    found_keys = []
    
    for filename in os.listdir('.'):
        if filename.endswith('.py'):
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                for pattern in api_key_patterns:
                    matches = re.findall(pattern, content)
                    if matches:
                        found_keys.append((filename, matches))
    
    if found_keys:
        print("   [X] FOUND HARDCODED API KEYS:")
        for filename, keys in found_keys:
            print(f"      {filename}: {len(keys)} key(s) found")
        return False
    else:
        print("   [OK] No hardcoded API keys found")
        return True

def check_required_files():
    """Check if all required files exist"""
    print("\n[*] Checking required files...")
    
    required_files = [
        'README.md',
        'LICENSE',
        '.gitignore',
        '.env.example',
        'requirements.txt',
        'CONTRIBUTING.md',
        'facebook_basic_scroll.py',
        'websitescraping.py',
    ]
    
    missing_files = []
    for filename in required_files:
        if not os.path.exists(filename):
            missing_files.append(filename)
    
    if missing_files:
        print("   [X] Missing required files:")
        for filename in missing_files:
            print(f"      - {filename}")
        return False
    else:
        print(f"   [OK] All {len(required_files)} required files present")
        return True

def check_env_file():
    """Check if .env file exists (should not be committed)"""
    print("\n[*] Checking for .env file...")
    
    if os.path.exists('.env'):
        print("   [!] WARNING: .env file found!")
        print("      This file should NOT be committed to GitHub")
        print("      Make sure it's in .gitignore")
        return False
    else:
        print("   [OK] No .env file found (good!)")
        return True

def check_gitignore():
    """Check if .gitignore contains important patterns"""
    print("\n[*] Checking .gitignore...")
    
    if not os.path.exists('.gitignore'):
        print("   [X] .gitignore file not found")
        return False
    
    with open('.gitignore', 'r', encoding='utf-8') as f:
        content = f.read()
    
    required_patterns = ['.env', '__pycache__', '*.pyc', 'data/']
    missing_patterns = [p for p in required_patterns if p not in content]
    
    if missing_patterns:
        print("   [!] Missing important patterns:")
        for pattern in missing_patterns:
            print(f"      - {pattern}")
        return False
    else:
        print("   [OK] .gitignore properly configured")
        return True

def check_readme():
    """Check if README has been customized"""
    print("\n[*] Checking README.md...")
    
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for placeholder text
    placeholders = ['YOUR_USERNAME', 'your.email@example.com', 'yourusername']
    found_placeholders = [p for p in placeholders if p in content]
    
    if found_placeholders:
        print("   [!] Found placeholder text in README:")
        for placeholder in found_placeholders:
            print(f"      - {placeholder}")
        print("      Consider updating these before publishing")
        return True  # Not critical, just a warning
    else:
        print("   [OK] README looks good")
        return True

def check_file_sizes():
    """Check for unusually large files"""
    print("\n[*] Checking file sizes...")
    
    large_files = []
    for filename in os.listdir('.'):
        if os.path.isfile(filename):
            size = os.path.getsize(filename)
            if size > 1_000_000:  # 1 MB
                large_files.append((filename, size))
    
    if large_files:
        print("   [!] Large files found:")
        for filename, size in large_files:
            print(f"      - {filename}: {size / 1_000_000:.2f} MB")
        print("      Consider if these should be committed")
        return True  # Not critical
    else:
        print("   [OK] No unusually large files")
        return True

def main():
    """Run all verification checks"""
    print("=" * 60)
    print("GitHub Publication Verification")
    print("=" * 60)
    
    checks = [
        ("API Keys", check_api_keys),
        ("Required Files", check_required_files),
        ("Environment File", check_env_file),
        ("Gitignore", check_gitignore),
        ("README", check_readme),
        ("File Sizes", check_file_sizes),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"   ❌ Error during {name} check: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Verification Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} - {name}")
    
    print("\n" + "=" * 60)
    
    if passed == total:
        print("ALL CHECKS PASSED!")
        print("[OK] Your package is ready for GitHub publication!")
        print("\nNext steps:")
        print("1. Create a GitHub repository")
        print("2. Run: git init")
        print("3. Run: git add .")
        print("4. Run: git commit -m 'Initial commit'")
        print("5. Run: git remote add origin <your-repo-url>")
        print("6. Run: git push -u origin main")
        print("\nSee GITHUB_SETUP.md for detailed instructions.")
        return 0
    else:
        print(f"[!] {total - passed} check(s) failed")
        print("Please fix the issues above before publishing.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

