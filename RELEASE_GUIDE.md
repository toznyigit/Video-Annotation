# Release & Update Guide

This document outlines the standard release and update procedure for the **Video Annotation Tool**. Follow this checklist whenever code, features, or fixes are introduced to ensure that the **User Manual** and **Platform Executables** remain synchronized.

---

## 1. Version Update Checklist

Whenever you make changes to the tool:

1. **Update Application Code & Front-facing Version**:
   - Update `__version__ = "X.Y.Z"` in `video_annotator.py`.
2. **Update the User Manual (`USER_MANUAL.md`)**:
   - Add/update any new settings, shortcuts, or workflows.
   - Update the version number and date at the top of `USER_MANUAL.md`.
3. **Update the In-App Help dialog**:
   - Ensure the in-app manual and "About" dialog reflect the current version.
4. **Commit the Changes**:
   ```bash
   git add .
   git commit -m "Release vX.Y.Z: <Summary of changes>"
   ```

---

## 2. Generating Executables

### Option A: Automatic Generation via GitHub Actions (Recommended)

When you push a version tag to GitHub:
```bash
git tag v1.0.1
git push origin v1.0.1
```
The automated CI/CD pipeline ([`.github/workflows/build.yml`](.github/workflows/build.yml)) will:
1. Spin up a Windows cloud machine and build `VideoAnnotator.exe`.
2. Spin up a macOS cloud machine and build `VideoAnnotator.app`.
3. Automatically attach both standalone zip files along with `USER_MANUAL.md` and `LICENSE` to the GitHub Release.

---

### Option B: Local Generation

If you need to produce the executables manually on local developer machines:

#### On macOS:
```bash
./build_mac.sh
```
- Produces: `dist/VideoAnnotator.app` and `dist/VideoAnnotator-macOS.zip`

#### On Windows:
```cmd
build_windows.bat
```
- Produces: `dist/VideoAnnotator.exe` and `dist/VideoAnnotator-Windows.zip`

---

## 3. Verification Checklist Before Distributing

- [ ] Video playback and pause work correctly on sample files.
- [ ] Questions load from `.txt` without encoding issues.
- [ ] Export to `.xlsx` generates valid file with headers and styling.
- [ ] `USER_MANUAL.md` matches the actual behavior and UI buttons.
- [ ] GPL-3 `LICENSE` is bundled with all distributed packages.
