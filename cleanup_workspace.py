#!/usr/bin/env python3
"""
Background Remover - Workspace Cleanup Script
Automatically removes unnecessary files and organizes the workspace
"""

import os
import shutil
import glob
from pathlib import Path
import datetime

def create_backup_folder():
    """Create a backup folder for files being removed"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_folder = f"_cleanup_backup_{timestamp}"
    os.makedirs(backup_folder, exist_ok=True)
    return backup_folder

def move_to_backup(file_path, backup_folder):
    """Move file to backup folder instead of deleting"""
    if os.path.exists(file_path):
        try:
            backup_path = os.path.join(backup_folder, os.path.basename(file_path))
            shutil.move(file_path, backup_path)
            return True
        except Exception as e:
            print(f"  ⚠️  Failed to backup {file_path}: {e}")
            return False
    return False

def remove_build_artifacts():
    """Remove PyInstaller build artifacts and cache"""
    print("🗂️  Removing build artifacts and cache...")

    removed_count = 0

    # Remove build directory (PyInstaller cache)
    if os.path.exists("build"):
        try:
            shutil.rmtree("build")
            print("  ✅ Removed build/ directory")
            removed_count += 1
        except Exception as e:
            print(f"  ⚠️  Could not remove build/: {e}")

    # Remove __pycache__ directories
    for pycache in glob.glob("**/__pycache__", recursive=True):
        try:
            shutil.rmtree(pycache)
            print(f"  ✅ Removed {pycache}")
            removed_count += 1
        except Exception as e:
            print(f"  ⚠️  Could not remove {pycache}: {e}")

    # Remove .pyc files
    for pyc_file in glob.glob("**/*.pyc", recursive=True):
        try:
            os.remove(pyc_file)
            print(f"  ✅ Removed {pyc_file}")
            removed_count += 1
        except Exception as e:
            print(f"  ⚠️  Could not remove {pyc_file}: {e}")

    return removed_count

def cleanup_redundant_source_files(backup_folder):
    """Remove redundant source files, keeping only the current versions"""
    print("\n📁 Cleaning up redundant source files...")

    removed_count = 0

    # Files to remove from src/ - keeping only current versions
    redundant_files = [
        "src/main_clean.py",      # Replaced by main_optimized.py
        "src/main_fresh.py",      # Replaced by main_optimized.py
        "src/gui_loader.py",      # Replaced by loader_window.py
        "src/gui_loader_new.py",  # Replaced by loader_window.py
        "src/bg_remove.py",       # Replaced by bg_remove_optimized.py
    ]

    for file_path in redundant_files:
        if move_to_backup(file_path, backup_folder):
            print(f"  ✅ Moved {file_path} to backup")
            removed_count += 1
        else:
            print(f"  ℹ️  {file_path} not found (already clean)")

    return removed_count

def cleanup_old_build_configs(backup_folder):
    """Remove old build configuration files"""
    print("\n⚙️  Cleaning up old build configurations...")

    removed_count = 0

    # Keep build.spec, remove others
    old_build_configs = [
        "build_fresh.spec",
        "build_optimized.spec",
        "test_build.spec",
    ]

    for file_path in old_build_configs:
        if move_to_backup(file_path, backup_folder):
            print(f"  ✅ Moved {file_path} to backup")
            removed_count += 1

    return removed_count

def cleanup_test_files(backup_folder):
    """Remove development and test files"""
    print("\n🧪 Cleaning up test and development files...")

    removed_count = 0

    # Test and development files to remove
    test_files = [
        "test_app_working.py",
        "test_functionality.py",
        "test_basic.py",
        "test_rembg.py",
        "test_context_menu.py",
        "test.py",
        "test_app.bat",
        "test_executable.bat",
        "final_verification.py",
        "2F3A0941-1.jpg",        # Test image
        "setup.py",              # Old setup script
        "setup_fixed.bat",
    ]

    for file_path in test_files:
        if move_to_backup(file_path, backup_folder):
            print(f"  ✅ Moved {file_path} to backup")
            removed_count += 1

    return removed_count

def cleanup_context_menu_fix_files(backup_folder):
    """Clean up context menu fix files (keep essential ones)"""
    print("\n🔧 Cleaning up context menu fix files...")

    removed_count = 0

    # Keep fix_context_menu.py and check_registry.py for troubleshooting
    # Remove the rest
    context_menu_files = [
        "fix_context_menu.reg",
        "fix_context_menu_admin.bat",
        "fix_context_menu_admin.ps1",
        "apply_context_menu_fix.bat",
    ]

    for file_path in context_menu_files:
        if move_to_backup(file_path, backup_folder):
            print(f"  ✅ Moved {file_path} to backup")
            removed_count += 1

    return removed_count

def organize_documentation(backup_folder):
    """Move development documentation to docs folder"""
    print("\n📚 Organizing documentation...")

    # Create docs folder
    os.makedirs("docs", exist_ok=True)

    moved_count = 0

    # Documentation to move to docs/
    doc_files = [
        "REFACTORING_SUMMARY.md",
        "EXECUTABLE_FIX.md",
        "RESOLUTION.md",
        "STATUS.md",
        "FREEMIUM_COMPLETE.md",
        "PAYPAL_STYLE_COMPLETE.md",
        "POSITIONING_SUCCESS.md",
        "PROJECT_COMPLETE.md",
        "BITMAP_TROUBLESHOOTING.md",
        "BUTTON_POSITIONING_FIX.md",
        "CODE_SIGNING_GUIDE.md",
        "INNO_SETUP_FIX.md",
        "INSTALLER_FIXES.md",
        "FALSE_POSITIVE_RESOLUTION.md",
        "WINDOWS_DEFENDER_FIX.md",
        "CONTEXT_MENU_FIX_COMPLETE.md",
    ]

    for file_path in doc_files:
        if os.path.exists(file_path):
            try:
                dest_path = os.path.join("docs", os.path.basename(file_path))
                shutil.move(file_path, dest_path)
                print(f"  ✅ Moved {file_path} to docs/")
                moved_count += 1
            except Exception as e:
                print(f"  ⚠️  Could not move {file_path}: {e}")

    return moved_count

def cleanup_batch_files(backup_folder):
    """Clean up old batch files"""
    print("\n📄 Cleaning up old batch files...")

    removed_count = 0

    # Keep essential batch files, remove others
    old_batch_files = [
        "build.bat",
        "check_installer_ready.bat",
    ]

    for file_path in old_batch_files:
        if move_to_backup(file_path, backup_folder):
            print(f"  ✅ Moved {file_path} to backup")
            removed_count += 1

    return removed_count

def keep_only_latest_executable():
    """Keep only the latest executable in dist/"""
    print("\n💾 Cleaning up dist/ folder...")

    if not os.path.exists("dist"):
        print("  ℹ️  dist/ folder not found")
        return 0

    exe_files = glob.glob("dist/*.exe")
    if len(exe_files) <= 1:
        print(f"  ℹ️  Only {len(exe_files)} executable found, nothing to clean")
        return 0

    # Sort by modification time, keep newest
    exe_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

    removed_count = 0
    for exe_file in exe_files[1:]:  # Keep first (newest), remove others
        try:
            os.remove(exe_file)
            print(f"  ✅ Removed old executable: {exe_file}")
            removed_count += 1
        except Exception as e:
            print(f"  ⚠️  Could not remove {exe_file}: {e}")

    return removed_count

def print_final_structure():
    """Print the cleaned workspace structure"""
    print("\n📋 Clean workspace structure:")
    print("=" * 50)

    essential_files = [
        "src/main_optimized.py",
        "src/bg_remove_optimized.py",
        "src/loader_window.py",
        "src/support_dialog.py",
        "src/gui_styles.py",
        "src/window_utils.py",
        "src/context_menu.py",
        "assets/icon.ico",
        "output/BackgroundRemover_Setup.exe",
        "dist/BackgroundRemover.exe",
        "build.spec",
        "installer_config.iss",
        "LICENSE.txt",
        "USER_GUIDE.txt",
        "README.md",
        "version_info.txt",
    ]

    print("\n✅ Essential files kept:")
    for file_path in essential_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"  📄 {file_path} ({size:,} bytes)")
        else:
            print(f"  ❓ {file_path} (not found)")

    # Count total files before and after
    total_files_now = sum([len(files) for r, d, files in os.walk(".")])
    print(f"\n📊 Workspace now has ~{total_files_now} files")

def main():
    print("🧹 Background Remover - Workspace Cleanup")
    print("=" * 45)
    print()

    # Create backup folder
    backup_folder = create_backup_folder()
    print(f"📦 Created backup folder: {backup_folder}")
    print("   (Files will be moved here instead of deleted)")
    print()

    total_removed = 0

    # Step 1: Remove build artifacts
    total_removed += remove_build_artifacts()

    # Step 2: Clean redundant source files
    total_removed += cleanup_redundant_source_files(backup_folder)

    # Step 3: Clean old build configs
    total_removed += cleanup_old_build_configs(backup_folder)

    # Step 4: Clean test files
    total_removed += cleanup_test_files(backup_folder)

    # Step 5: Clean context menu fix files
    total_removed += cleanup_context_menu_fix_files(backup_folder)

    # Step 6: Clean batch files
    total_removed += cleanup_batch_files(backup_folder)

    # Step 7: Organize documentation
    moved_docs = organize_documentation(backup_folder)

    # Step 8: Clean dist folder
    total_removed += keep_only_latest_executable()

    # Summary
    print(f"\n🎉 Cleanup completed!")
    print(f"   📤 {total_removed} files removed/moved to backup")
    print(f"   📚 {moved_docs} documentation files organized to docs/")
    print(f"   🗂️  Backup folder: {backup_folder}")

    # Show final structure
    print_final_structure()

    print(f"\n💡 Next steps:")
    print(f"   1. Test that BackgroundRemover.exe still works")
    print(f"   2. If everything works, you can delete: {backup_folder}")
    print(f"   3. Your workspace is now clean and organized!")

if __name__ == "__main__":
    main()
