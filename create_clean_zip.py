"""Create a clean zip archive of the SARTA codebase.

Excludes:
- node_modules, .next (Frontend dependencies & build artifacts)
- __pycache__, .pytest_cache, *.pyc (Python bytecode)
- venv, .venv, env (Virtual environments)
- .git (Git version control history)
- backend/.env, *.sqlite3, *.db (Sensitive secrets and local databases)
- Existing .zip archives
"""

import os
import zipfile
from pathlib import Path

# Directories to exclude
EXCLUDE_DIRS = {
    'node_modules',
    '.next',
    '__pycache__',
    '.pytest_cache',
    '.git',
    'venv',
    '.venv',
    'env',
}

# Sensitive or temporary files to exclude
EXCLUDE_FILES = {
    '.env',
    'assessment_sessions.sqlite3',
    'skill_tree.db',
}

# File extensions to exclude
EXCLUDE_EXTS = {
    '.pyc',
    '.pyo',
    '.sqlite3',
    '.zip',
}

def create_zip(output_filename="SARTA_clean.zip", include_pptx=True):
    root_dir = Path(__file__).resolve().parent
    output_path = root_dir / output_filename
    
    file_count = 0
    print(f"Creating clean zip archive: {output_filename}...")

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zip_out:
        for path in root_dir.rglob('*'):
            # Skip excluded directories
            if any(part in EXCLUDE_DIRS for part in path.parts):
                continue
            
            # Skip excluded files or extensions
            if path.name in EXCLUDE_FILES or path.suffix.lower() in EXCLUDE_EXTS:
                continue

            # Optional pptx toggle
            if not include_pptx and path.suffix.lower() == '.pptx':
                continue

            if path.is_file() and path != output_path:
                arcname = path.relative_to(root_dir)
                zip_out.write(path, arcname)
                file_count += 1

    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"Successfully archived {file_count} files into '{output_filename}' ({size_mb:.2f} MB).")
    print("Excluded: node_modules, .next, __pycache__, .git, and private .env secrets.")

if __name__ == "__main__":
    create_zip()

