# Video Annotation Tool — User Manual

**Version:** 1.0.0  
**License:** GNU General Public License v3.0 ([GPL-3.0](file:///Users/tameryigit/Documents/AG_Projects/V/video_iter_2/LICENSE))  
**Platforms:** macOS, Windows, Linux  

---

## 1. Overview

The **Video Annotation Tool** is an interactive desktop application designed for researchers, annotators, and clinicians to systematically review video recordings at defined time intervals and log qualitative or quantitative observations.

### Key Features
- **Frame-by-Frame Interval Stepping:** Step through video sequences automatically using custom step sizes (e.g., every 0.5s, 1s, 2s, etc.).
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
| **macOS** | Unzip `VideoAnnotator-macOS.zip`, open `Video Annotator.app` (or run `dist/VideoAnnotator`). If macOS displays a Gatekeeper prompt on first launch, right-click the app and choose **Open**. |
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

## 5. Interface Guide

```
+───────────────────────────────────────────────+───────────────────────────────────────────────+
|                  LEFT PANEL                   |                  RIGHT PANEL                  |
+───────────────────────────────────────────────+───────────────────────────────────────────────+
| [ Video Preview Window ]                      | [ Current Question Box ]                      |
|                                               | Question 1 / 4                                |
| Timestamp: 00:01:15 / 00:10:00                | "Is the subject looking at the screen?"       |
|                                               | [ Answer Input Area ........................] |
| [ Load Files ]                                | [ Next Question > ]  [ Skip ]                 |
| Video:     [ path/video.mp4      ] [Browse]   +───────────────────────────────────────────────+
| Questions: [ path/questions.txt  ] [Browse]   | [ Annotation Records Table ]                  |
|                                               | Video | Label | Timestamp | Step | Q | A      |
| [ Session Settings ]                          | --------------------------------------------- |
| Start (s): [ 0   ]  End (s): [ 120 ]          | vid.mp4 | Mother | 0:00:01 | 1 | ... | Yes    |
| Step (s):  [ 1.0 ]  Label:   [ Mother v ] ●   +───────────────────────────────────────────────+
|                                               | [ ⬇ Export to Excel ]    [ 🗑 Clear Table ]   |
| [ ▶ Start Processing ]     [ ■ Stop ]         |                                               |
| Status: Ready.                                |                                               |
+───────────────────────────────────────────────+───────────────────────────────────────────────+
```

---

## 6. Step-by-Step Annotation Workflow

### Step 1: Load Media & Questions
1. Click **Browse Video** and select your video file.
   - The video will load in the preview player.
   - The total duration will automatically populate the **End (s)** setting.
2. Click **Browse Questions** and select your `.txt` questions file.
   - The status bar will confirm: `Loaded X questions.`

### Step 2: Configure Session Settings
- **Start (s):** Starting second of the video to begin annotating (default: `0`).
- **End (s):** Ending second of the video (defaults to total video length).
- **Step (s):** Interval step between questions (e.g., `1.0` for 1 second, `0.5` for half a second).
- **Label:** Select the participant role being annotated:
  - **Mother** (Orange badge)
  - **Child** (Teal badge)

### Step 3: Start Annotation
1. Click **▶ Start Processing**.
2. The video will advance to the start time, pause on the target frame, and present the first question in the right-hand panel.

### Step 4: Answer Questions
1. Type your response in the answer box.
2. Press **Next Question ›** (or press <kbd>Ctrl</kbd> + <kbd>Enter</kbd>).
3. Repeat for all questions assigned to this step.
4. If a question is not applicable, click **Skip** to leave it blank.
5. Once the last question is submitted, all answers for that timestamp are committed to the **Annotation Records** table, and the video automatically advances by your chosen step size.

### Step 5: Complete & Export
- Once the end time is reached, an alert confirms the completion of the session.
- Click **⬇ Export to Excel** to save the formatted `.xlsx` workbook.
- The exported file includes:
  - **Video Title**
  - **Label** (Mother / Child)
  - **Timestamp** (`HH:MM:SS`)
  - **Step #**
  - **Question**
  - **Answer**

---

## 7. Keyboard Shortcuts & Quick Tips

| Action | Shortcut / Tip |
| :--- | :--- |
| **Submit Answer & Next Question** | Click **Next Question ›** or press <kbd>Ctrl</kbd> + <kbd>Return</kbd> / <kbd>Cmd</kbd> + <kbd>Return</kbd> |
| **Stop Session Early** | Click **■ Stop** anytime to pause the session and keep recorded data intact |
| **Clear Records** | Click **🗑 Clear Table** to reset the data table for a fresh session |
| **Change Label Mid-Session** | You can adjust the **Label** dropdown before starting a new step or pass |

---

## 8. Troubleshooting & FAQ

#### Q: The video does not play or shows a black screen.
- **Cause:** Unsupported media codec or missing OS media framework.
- **Solution:** Ensure the video is encoded with standard **H.264 video** and **AAC audio**. Free tools like HandBrake or `ffmpeg` (`ffmpeg -i input.mov -c:v libx264 -c:a aac output.mp4`) can convert videos cleanly.

#### Q: On macOS, I get a security warning: "Video Annotator can't be opened because it is from an unidentified developer".
- **Solution:** Right-click `Video Annotator.app`, select **Open**, and click **Open** in the dialog. Alternatively, open **System Settings > Privacy & Security** and click **Open Anyway**.

#### Q: Excel export gives a CSV file instead of `.xlsx`.
- **Cause:** The `openpyxl` Python library is missing in your environment.
- **Solution:** Run `pip install openpyxl` or use the precompiled standalone executable which includes `openpyxl` out of the box.

---

## 9. License

This program is free software: you can redistribute it and/or modify it under the terms of the **GNU General Public License** as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

See the [LICENSE](file:///Users/tameryigit/Documents/AG_Projects/V/video_iter_2/LICENSE) file for details.
