import os
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Set

# --- Default Exclusion Rules ---
# You can add more patterns here if needed.
EXCLUDE_EXTENSIONS = {'.pyc', '.log', '.env', '.lock', '.DS_Store'}
EXCLUDE_FILENAMES = {'.gitignore', '.gitattributes'}
EXCLUDE_PATTERNS = {'__pycache__', '.git', 'node_modules', 'dist', 'build'}

def _is_binary(content: bytes) -> bool:
    """A simple heuristic to check if content is binary."""
    return b'\0' in content

def _generate_file_tree(paths: List[str], project_root: str) -> str:
    """Generates a string representation of the file tree."""
    tree = ["📁 Root"]
    structure = {}
    for path_str in sorted(paths):
        # Create relative paths for the tree structure
        relative_path = os.path.relpath(path_str, project_root)
        parts = relative_path.split(os.sep)
        current_level = structure
        for part in parts:
            current_level = current_level.setdefault(part, {})

    def build_tree(level_structure, indent=""):
        for name in sorted(level_structure.keys()):
            is_dir = bool(level_structure[name])
            icon = "📁" if is_dir else "📄"
            tree.append(f"{indent}{icon} {name}")
            if is_dir:
                build_tree(level_structure[name], indent + "  ")

    build_tree(structure)
    return "\n".join(tree)

def _get_project_files(project_root: str, exclude_patterns: Set[str]) -> List[str]:
    """Walks the project directory and returns a list of non-excluded files."""
    filepaths = []
    for root, dirs, files in os.walk(project_root, topdown=True):
        # Exclude directories by modifying dirs in-place
        dirs[:] = [d for d in dirs if d not in exclude_patterns]

        for file in files:
            filepath = os.path.join(root, file)
            path_obj = Path(filepath)
            
            # Normalize for pattern matching
            normalized_path = path_obj.as_posix()

            if (path_obj.name in EXCLUDE_FILENAMES or
                path_obj.suffix.lower() in EXCLUDE_EXTENSIONS or
                any(pattern in normalized_path for pattern in exclude_patterns)):
                continue
            
            filepaths.append(filepath)
    return filepaths

def _calculate_directory_hash(filepaths: List[str]) -> str:
    """Calculates a single hash for all file contents and names."""
    hasher = hashlib.sha256()
    for filepath in sorted(filepaths):
        try:
            with open(filepath, 'rb') as f:
                # Hash the relative path to account for renames/moves
                relative_path = os.path.relpath(filepath).encode('utf-8')
                hasher.update(relative_path)
                # Hash the file content
                hasher.update(f.read())
        except IOError:
            # Ignore files that can't be read
            continue
    return hasher.hexdigest()

def document_project(output_dir: str, project_root: str = None, filename_prefix: str = "documentation") -> Optional[str]:
    """
    Generates a Markdown document for the project if changes are detected.

    Args:
        output_dir: The directory where documentation will be saved.
                    This directory is ALWAYS excluded from the scan.
        project_root: The root directory of the project to scan.
                      Defaults to the current working directory.
        filename_prefix: The prefix for the generated Markdown file.

    Returns:
        The full path to the new documentation file if it was created,
        otherwise None.
    """
    if project_root is None:
        project_root = os.getcwd()

    # --- State Management ---
    output_path = Path(output_dir)
    state_file = output_path / ".doc_state"
    last_hash = None
    if state_file.exists():
        with open(state_file, 'r') as f:
            last_hash = f.read().strip()
    
    # --- Hash Calculation ---
    # Crucially, add the output directory to the exclusion patterns
    current_exclude_patterns = EXCLUDE_PATTERNS.copy()
    current_exclude_patterns.add(output_path.name)

    all_files = _get_project_files(project_root, current_exclude_patterns)
    current_hash = _calculate_directory_hash(all_files)

    # --- Change Detection ---
    if current_hash == last_hash:
        return None # No changes, do nothing.

    # --- Markdown Generation ---
    markdown_content = []
    project_name = os.path.basename(os.path.abspath(project_root))
    markdown_content.append(f"# Project Documentation: {project_name}\n")
    
    markdown_content.append("## File Structure\n")
    markdown_content.append("```\n")
    markdown_content.append(_generate_file_tree(all_files, project_root))
    markdown_content.append("```\n\n")

    markdown_content.append("## File Contents\n")
    markdown_content.append("Below are the contents of all files in the project:\n\n")

    for filepath in all_files:
        relative_path = os.path.relpath(filepath, project_root)
        file_extension = Path(filepath).suffix[1:].lower() or 'text'
        
        markdown_content.append(f"### File: {relative_path}\n")
        
        try:
            with open(filepath, 'rb') as f:
                content_raw = f.read()

            if _is_binary(content_raw):
                markdown_content.append(f"[Binary file - {len(content_raw)} bytes]\n\n")
            else:
                text_content = content_raw.decode('utf-8', errors='replace')
                markdown_content.append(f"```{file_extension}\n")
                markdown_content.append(text_content)
                markdown_content.append("\n```\n\n")
        except Exception as e:
            markdown_content.append(f"[Error reading file: {e}]\n\n")

    # --- Save Output and State ---
    os.makedirs(output_path, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_filename = f"{filename_prefix}_{timestamp}.md"
    output_filepath = output_path / output_filename
    
    with open(output_filepath, 'w', encoding='utf-8') as f:
        f.write("".join(markdown_content))
        
    with open(state_file, 'w') as f:
        f.write(current_hash)
        
    return str(output_filepath)
