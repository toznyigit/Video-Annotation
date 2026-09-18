# Video Annotation Tool — User Manual

**Version:** 1.1.0  
**License:** GNU General Public License v3.0 ([GPL-3.0](file:///Users/tameryigit/Documents/AG_Projects/V/video_iter_2/LICENSE))  
**Platforms:** macOS, Windows, Linux  

---

## 1. Overview

The **Video Annotation Tool** is an interactive desktop application designed for researchers, annotators, and clinicians to systematically review video recordings at defined time intervals and log qualitative or quantitative observations.

### Key Features
- **Frame-by-Frame Interval Stepping:** Step through video sequences automatically using customizable step sizes.
- **Quick Step Presets:** Instant selection of common step intervals (**0.5s**, **1s**, **5s**, **10s**) plus fully free-form custom input.
- **Full Screen Annotation Mode:** Expand the video to full screen with an integrated, glassmorphic **floating HUD** for questions and answers without leaving full screen.
- **Resizable Video Display:** Flexible split pane allows users to resize the video and annotation panels freely.
- **Interactive Question Prompts:** Cycle through predefined questions loaded from a plain text file at each step.
- **Participant Categorization:** Tag annotations with distinct labels (e.g., **Mother** vs. **Child**) with color-coded UI badges.
- **Live Annotation Table:** Immediate visual verification of recorded responses.
- **Professional Excel Export:** One-click formatted `.xlsx` export with freeze panes, auto-fitted columns, and color-coded rows (with fallback to `.csv`).
- **Zero-Python Standalone Executables:** Ready-to-use native packages for macOS and Windows.

---

## 2. System Requirements

- **Operating System:**
  - **macOS:** macOS 11.0 (Big Sur) or higher (Apple Silicon and Intel supported).
  - **Windows:** Windows 10 or Windows 11 (64-bit).
  - **Linux:** Any modern distribution with Qt6/X11 or Wayland support.
- **Hardware:** Minimum 4 GB RAM, 500 MB free disk space.
- **Python (Optional):** Python 3.9 – 3.14. *Not required if using the standalone precompiled executables.*

---

## 3. Installation & Launching

You can run the Video Annotation Tool in two ways:

### Option A: Standalone Executable (Recommended — No Python Required)

| Platform | How to Run |
| :--- | :--- |
| **macOS** | Unzip `VideoAnnotator-macOS.zip` and open `VideoAnnotator.app`. (If blocked by Gatekeeper: Open **System Settings** → **Privacy & Security** → scroll down to **Security** → click **Open Anyway**, or run `xattr -cr VideoAnnotator.app` in Terminal). |
| **Windows** | Double-click `VideoAnnotator.exe`. No installation or Python setup is necessary. |

---

### Option B: One-Click Launch Script (Source Code)

If you have downloaded or cloned the repository source code:

- **macOS / Linux:**
  1. Open Terminal in the project folder.
  2. Run:
     ```bash
     ./run.sh
     ```
  *(The script automatically configures a `.venv` virtual environment, installs any missing packages, and launches the app.)*

- **Windows:**
  1. Double-click `run.bat` (or open Command Prompt / PowerShell and type `run.bat`).
  *(The script detects Python, prepares the `.venv`, installs requirements, and opens the application.)*

---

### Option C: Manual Python Setup (Terminal)

```bash
# 1. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate       # On Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch
python video_annotator.py
```

---

## 4. Preparing Your Files

### 1. Video Files
Supported formats: `.mp4`, `.avi`, `.mkv`, `.mov`, `.wmv`, `.flv`, `.webm`.  
Ensure standard video codecs (e.g., H.264 / AAC) are used for optimal seeking performance.

### 2. Questions File (`.txt`)
Create a standard plain text file (`.txt`) containing the questions you want to ask at each video interval.  
**Rule:** Each question must be on its own line. Blank lines are ignored.

**Example `questions.txt`:**
```text
Is the subject looking at the screen?
What emotional expression is observed?
Is there verbal communication?
Rate the engagement level (1-5):
```

---

## 5. Interface & Layout Guide

```text
+───────────────────────────────────────────────────────────────────────────────────────────────+
| 🎬 Video Annotation Tool  v1.1.0 • GPL-3.0                   [📖 User Manual]  [⚖️ About]     |
+───────────────────────────────────────────────+───────────────────────────────────────────────+
|                  LEFT PANEL                   |                  RIGHT PANEL                  |
+───────────────────────────────────────────────+───────────────────────────────────────────────+
| [ Video Preview Window (Double-click: Fullscreen) ]                                           |
| 00:01:15 / 00:10:00        [ ⛶ Full Screen ]  | [ Current Question Box ]                      |
|                                               | Question 1 / 4                                |
| [ Load Files ]                                | "Is the subject looking at the screen?"       |
| Video:     [ path/video.mp4      ] [Browse]   | [ Answer Input Area ........................] |
| Questions: [ path/questions.txt  ] [Browse]   | [ Next Question > ]  [ Skip ]                 |
|                                               +───────────────────────────────────────────────+
| [ Session Settings ]                          | [ Annotation Records Table ]                  |
| Start (s): [ 0   ]  End (s): [ 120 ]          | Video | Label | Timestamp | Step | Q | A      |
| Step Presets: [ 0.5s ] [ 1s ] [ 5s ] [ 10s ]  | --------------------------------------------- |
| Custom Step: [ 1.0 ]s  Label: [ Mother v ] ●  | vid.mp4 | Mother | 0:00:01 | 1 | ... | Yes    |
|                                               +───────────────────────────────────────────────+
| [ ▶ Start Processing ]     [ ■ Stop ]         | [ ⬇ Export to Excel ]    [ 🗑 Clear Table ]   |
| Status: Ready.                                |                                               |
+───────────────────────────────────────────────+───────────────────────────────────────────────+
```

---

## 6. Full Screen Mode & Floating HUD

The tool features a dedicated **Full Screen Annotation Mode**:
- **Entering Full Screen:** Click the **⛶ Full Screen** button under the video, press <kbd>F11</kbd>, or **double-click** anywhere on the video player.
- **Floating Controls (HUD):**
  - **Top Bar:** Shows the draggable handle (`⠿ Drag`), current timestamp, step counter (`Step 3 / 60`), an interactive **Participant Label Selector** (Mother / Child dropdown), and an **✕ Exit Full Screen (Esc)** button.
  - **Change Label Mid-Session:** Annotators can switch between **Mother** and **Child** directly from the floating questionnaire without leaving full screen.
  - **Floating Question Card:** An unobtrusive semi-transparent glassmorphic card overlays the screen displaying the current question, the answer input field, and equal-width **Next Question ›** and **Skip** buttons.
- **Submitting Answers in Full Screen:** Type your answer and press <kbd>Ctrl</kbd>+<kbd>Enter</kbd> (or <kbd>Cmd</kbd>+<kbd>Enter</kbd> on macOS) to instantly submit and cycle to the next question.
- **Exiting Full Screen:** Press <kbd>Esc</kbd>, press <kbd>F11</kbd>, or click **✕ Exit Full Screen**. The application returns to the standard side-by-side view without interrupting playback.

---

## 7. Step-by-Step Annotation Workflow

### Step 1: Load Media & Questions
1. Click **Browse Video** and select your video file.
   - The video loads into the player.
   - The duration automatically sets the **End (s)** setting.
2. Click **Browse Questions** and select your `.txt` file.
   - Status confirms: `Loaded X questions.`

### Step 2: Configure Session Settings & Step Presets
- **Start (s) & End (s):** Define the segment of the video to analyze.
- **Step Presets:** Click any of the quick preset buttons:
  - **0.5s** (Fine-grained micro-analysis)
  - **1.0s** (Standard 1-second cadence)
  - **5.0s** (5-second intervals)
  - **10.0s** (10-second intervals)
- **Custom Step (s):** You can also adjust the numeric box to any custom decimal value (e.g. `2.5s` or `15s`).
- **Label:** Select the participant role being coded (**Mother** or **Child**).

### Step 3: Start Processing
1. Click **▶ Start Processing**.
2. The video moves to the start frame, pauses, and shows the first question.
3. *(Optional)* Switch to **Full Screen** (<kbd>F11</kbd>) for focused annotation.

### Step 4: Record Responses
1. Type your response in the text area.
2. Press <kbd>Ctrl</kbd>+<kbd>Enter</kbd> / <kbd>Cmd</kbd>+<kbd>Enter</kbd> or click **Next Question ›**.
3. Use **Skip** if a question is not applicable.
4. When the last question for the current timestamp is completed, the records are appended to the table and the video automatically advances by your step size.

### Step 5: Complete & Export
- When the video reaches the end second, the session ends with a summary notification.
- Click **⬇ Export to Excel** to produce a styled `.xlsx` workbook featuring:
  - Video title and label
  - Exact timestamp (`HH:MM:SS`)
  - Step index number
  - Question text
  - Recorded answer
  - Role-colored rows and frozen header row

---

## 8. Keyboard Shortcuts & Quick Reference

| Action | Shortcut / Gesture |
| :--- | :--- |
| **Submit Answer & Next Question** | `Ctrl` + `Return` / `Cmd` + `Return` |
| **Toggle Full Screen Mode** | `F11` or **Double-Click Video** |
| **Exit Full Screen Mode** | `Escape` or `F11` |
| **Stop Session Early** | Click **■ Stop** (preserves already recorded data) |
| **Clear Records** | Click **🗑 Clear Table** |

---

## 9. Troubleshooting & FAQ

#### Q: How do I resize the video window?
- Drag the splitter bar between the left video panel and the right table panel. The video scales dynamically to fit whatever width you select.
- For maximum viewing area, use **Full Screen Mode** (<kbd>F11</kbd>).

#### Q: Can I change step intervals during a session?
- You can change step intervals before starting or stop the session, adjust the step preset, and restart from the current timestamp.

#### Q: Video does not play or shows a black screen.
- Ensure the video is encoded with standard **H.264 video** and **AAC audio**.

#### Q: On macOS, I see "VideoAnnotator.app can't be opened because Apple cannot check it for malicious software" or "unidentified developer".
Because this is an open-source application without an Apple Developer ID signature, macOS Gatekeeper blocks it by default on first launch. To permit and run it:
1. Open **System Settings** (from the  Apple menu).
2. Go to **Privacy & Security** in the left sidebar.
3. Scroll down to the **Security** section.
4. You will see a notification stating: *"VideoAnnotator.app was blocked from use because it is not from an identified developer"*.
5. Click **Open Anyway** and confirm by clicking **Open** (enter password or Touch ID if requested).
*(Alternatively, you can open Terminal and run `xattr -cr /path/to/VideoAnnotator.app` to clear the quarantine flag directly.)*

---

## 10. License

This program is free software: you can redistribute it and/or modify it under the terms of the **GNU General Public License** as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

See the [LICENSE](file:///Users/tameryigit/Documents/AG_Projects/V/video_iter_2/LICENSE) file for details.
