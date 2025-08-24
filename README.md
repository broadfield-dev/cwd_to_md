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
pip install git+https://github.com/your-username/cwd_to_md.git
