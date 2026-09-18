# Video Annotation Tool

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Windows%20%7C%20Linux-lightgrey.svg)](USER_MANUAL.md)
[![Python 3](https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue.svg)](https://www.python.org)
[![PyQt6](https://img.shields.io/badge/GUI-PyQt6-green.svg)](https://pypi.org/project/PyQt6/)

A modern, fast desktop video annotation tool designed for systematic video review, behavioral coding, and qualitative/quantitative research. Step through video intervals, answer prompt questions at designated timestamps, and export clean, formatted Excel reports.

---

## ✨ Features

- ⏱ **Interval Stepping:** Advance video at customizable step intervals (e.g., 0.5s, 1s, 2s).
- ❓ **Dynamic Questions:** Load any question list from plain text files (`.txt`).
- 🏷 **Subject Tagging:** Real-time role labeling (**Mother** / **Child**) with color differentiation.
- 📊 **Instant Table Review:** Monitor logged annotations live in a scrollable, sorted data table.
- 📑 **Formatted Excel Export:** Generates `.xlsx` files with colored headers, category-tinted rows, auto-sized columns, and frozen header panes (with automatic CSV fallback).
- ⚡ **Zero-Python Standalone Executables:** Ready-to-use binaries for **macOS** and **Windows** that work with no prior Python installation.
- 🎨 **Sleek Dark Theme:** High-contrast, eye-friendly modern interface built with PyQt6.

---

## 🚀 Quick Start

### 1. Standalone Executable (No Python Required)
Download the latest precompiled release for your operating system:
- **macOS:** Download `VideoAnnotator-macOS.zip` from [Releases](https://github.com), unzip and run `Video Annotator.app`.
- **Windows:** Download and double-click `VideoAnnotator.exe` from [Releases](https://github.com).

### 2. From Source Code

#### macOS / Linux
```bash
git clone https://github.com/your-username/video-annotator.git
cd video-annotator
./run.sh
```

#### Windows
```cmd
git clone https://github.com/your-username/video-annotator.git
cd video-annotator
run.bat
```

*(Both scripts will automatically configure a virtual environment, install requirements, and start the app.)*

---

## 📖 User Manual & Documentation

For a complete guide on how to prepare question files, navigate sessions, use shortcuts, and troubleshoot, read the [**Full User Manual**](USER_MANUAL.md).

You can also access the user manual directly inside the application by clicking the **📖 User Manual** button in the header bar.

---

## 🛠 Building Executables Locally

To generate standalone binaries locally on your computer using PyInstaller:

### macOS
```bash
./build_mac.sh
```
*Outputs `dist/Video Annotator.app` and `dist/VideoAnnotator-macOS.zip`.*

### Windows
```cmd
build_windows.bat
```
*Outputs `dist/VideoAnnotator.exe`.*

For automated builds on every GitHub release tag, see the included CI/CD workflow in [`.github/workflows/build.yml`](.github/workflows/build.yml) and the [**Release Guide**](RELEASE_GUIDE.md).

---

## 📄 License

This program is free software: you can redistribute it and/or modify it under the terms of the **GNU General Public License** as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

See the [LICENSE](LICENSE) file for details.
