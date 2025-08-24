# Current Working Directory to Markdown (cwd_to_md)

`cwd_to_md` is a lightweight, dependency-free Python utility that generates a comprehensive Markdown document from a project's directory structure and file contents.

It's designed to be called from within your own Python applications. It intelligently detects if any files have changed since the last run and only generates new documentation when an update is needed.

## Features

-   **Automatic Change Detection:** Uses file content hashing to determine if a documentation update is necessary, avoiding redundant work.
-   **Zero Dependencies:** Built entirely with Python's standard library for maximum portability and ease of integration.
-   **Automatic Versioning:** Saves each new documentation file with a timestamp, creating a simple version history.
-   **Safe Exclusion:** Automatically excludes its own output directory to prevent the documentation from including itself in future runs.
-   **Customizable:** You can specify the output directory, filename prefixes, and which files/folders to ignore.

## Installation

Install the package directly from GitHub using `pip`:

```bash
pip install git+https://github.com/broadfield-dev/cwd_to_md.git
```

## Usage

The primary use case is to call `document_project` from a script within your own project. It will scan the directory, and if it detects changes, it will generate a new, timestamped Markdown file.

Create a Python script in your project's root directory (e.g., `generate_docs.py`):

```python
# generate_docs.py
from cwd_to_md import document_project

def update_documentation():
    """
    Checks for project updates and generates a new documentation
    file if changes are found.
    """
    print("Checking for project file changes...")

    # The main function call:
    # - It will save docs to a folder named 'project_docs'.
    # - It will use '.doc_state' to store the last project hash.
    # - The 'project_docs' folder is automatically excluded.
    generated_file = document_project(
        output_dir="project_docs",
        filename_prefix="project_snapshot"
    )

    if generated_file:
        print(f"Project updated. New documentation saved to: {generated_file}")
    else:
        print("No changes detected. Documentation is up to date.")

if __name__ == "__main__":
    update_documentation()

```

To run it, simply execute the script from your terminal:
```bash
python generate_docs.py
```

The first time it runs, it will create `project_docs/` and save a file like `project_snapshot_2025-08-24_04-30-00.md`. It also creates a hidden `.doc_state` file in the output directory to store the project's "fingerprint" (hash).

On subsequent runs, it will only create a new file if you have modified, added, or deleted any source files.

## How It Works

1.  The `document_project` function first calculates a unique hash (a SHA-256 fingerprint) of all the file contents and names in the target directory, respecting the exclusion rules.
2.  It compares this new hash with the hash from the previous run, which is stored in the `.doc_state` file inside your specified `output_dir`.
3.  **If the hashes match**, the function does nothing and reports that the project is up to date.
4.  **If the hashes are different** (or if the state file doesn't exist), it proceeds to generate a new Markdown document with the current project state, saves it with a timestamp, and updates the `.doc_state` file with the new hash.

This makes the process highly efficient and ensures that documentation is only generated when necessary.
