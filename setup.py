from setuptools import setup
from pathlib import Path

here = Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(name="roku-tui",
        version="0.1.2",
        description="A TUI remote for Roku",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/winsbe01/roku-tui",
        author="Ben Winston",
        author_email="ben@benwinston.us",
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Environment :: Console :: Curses",
            "Intended Audience :: End Users/Desktop",
            "License :: OSI Approved :: Apache Software License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3 :: Only",
            "Topic :: Games/Entertainment",
            "Topic :: Utilities",
        ],
        keywords="roku, remote, tui, cli",
        py_modules=["roku_tui"],
        python_requires=">=3.7, <4",
        entry_points={
            "console_scripts": [
                "roku-tui=roku_tui:startup",
            ],
        },
        project_urls={
            "Source": "https://github.com/winsbe01/roku-tui",
        },
)
