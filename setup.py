from setuptools import setup, find_packages

setup(
    name="cwd_to_md",
    version="0.1.0",
    description="A dependency-free utility to generate a Markdown document from the current project directory, with change detection.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/your-username/cwd_to_md",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
