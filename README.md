# Video Annotation Tool

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Latest Release](https://img.shields.io/github/v/release/toznyigit/Video-Annotation?color=blue&label=Latest%20Release)](https://github.com/toznyigit/Video-Annotation/releases/latest)
[![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Windows%20%7C%20Linux-lightgrey.svg)](USER_MANUAL.md)
[![Python 3](https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue.svg)](https://www.python.org)
[![PyQt6](https://img.shields.io/badge/GUI-PyQt6-green.svg)](https://pypi.org/project/PyQt6/)

A modern, fast desktop video annotation tool designed for systematic video review, behavioral coding, and qualitative/quantitative research. Step through video intervals, answer prompt questions at designated timestamps, and export clean, formatted Excel reports.

---

## ✨ Features

- ⏱ **Interval Stepping:** Advance video at customizable step intervals with quick-click presets (**0.5s**, **1s**, **5s**, **10s**) plus custom intervals.
- ⛶ **Full Screen & Floating HUD:** Annotate in full-screen immersion with an integrated, translucent floating HUD for questions and answers.
- 📐 **Resizable Video Display:** Flexible split-pane layout to scale video and table panels to your preferred size.
- ❓ **Dynamic Questions:** Load any question list from plain text files (`.txt`).
- 🏷 **Subject Tagging:** Real-time role labeling (**Mother** / **Child**) with color differentiation.
- 📊 **Instant Table Review:** Monitor logged annotations live in a scrollable, sorted data table.
- 📑 **Formatted Excel Export:** Generates `.xlsx` files with colored headers, category-tinted rows, auto-sized columns, and frozen header panes (with automatic CSV fallback).
- ⚡ **Zero-Python Standalone Executables:** Ready-to-use binaries for **macOS** and **Windows** that work with no prior Python installation.
- 🎨 **Sleek Dark Theme:** High-contrast, eye-friendly modern interface built with PyQt6.

---

## 🚀 Quick Start

### 1. Standalone Executable (No Python Required)
Precompiled zero-dependency binaries are available directly from the **[GitHub Releases](https://github.com/toznyigit/Video-Annotation/releases)**:

- 🍏 **macOS:**
  - **Direct Download:** [**`VideoAnnotator-macOS.zip`**](https://github.com/toznyigit/Video-Annotation/releases/latest/download/VideoAnnotator-macOS.zip)
  - Alternatively, download from the [Latest Release Page](https://github.com/toznyigit/Video-Annotation/releases/latest). Unzip and run `VideoAnnotator.app`.
- 🪟 **Windows:**
  - **Direct Download:** [**`VideoAnnotator-Windows.zip`**](https://github.com/toznyigit/Video-Annotation/releases/latest/download/VideoAnnotator-Windows.zip)
  - Alternatively, download from the [Latest Release Page](https://github.com/toznyigit/Video-Annotation/releases/latest). Unzip and double-click `VideoAnnotator.exe`.

📦 **All Versions & Changelogs:** [Browse all GitHub Releases](https://github.com/toznyigit/Video-Annotation/releases)

### 2. From Source Code

#### macOS / Linux
```bash
git clone https://github.com/toznyigit/Video-Annotation.git
cd Video-Annotation
./run.sh
```

#### Windows
```cmd
git clone https://github.com/toznyigit/Video-Annotation.git
cd Video-Annotation
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
