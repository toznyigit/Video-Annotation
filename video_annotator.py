# ==============================================================================
# Video Annotation Tool
# Copyright (C) 2026 Tamer Yigit and contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ==============================================================================

import sys
import os
import csv
from datetime import timedelta

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFileDialog, QLineEdit, QComboBox,
    QTableWidget, QTableWidgetItem, QSplitter, QGroupBox,
    QSpinBox, QDoubleSpinBox, QTextEdit, QMessageBox, QHeaderView,
    QDialog, QTextBrowser, QSizePolicy, QFrame, QGridLayout,
    QGraphicsDropShadowEffect,
)
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import Qt, QUrl, QTimer, QEvent, pyqtSignal, QPoint
from PyQt6.QtGui import QFont, QColor, QDesktopServices

try:
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    OPENPYXL_AVAILABLE = True
except ImportError:
    OPENPYXL_AVAILABLE = False

__version__ = "1.1.0"

# ── Modern Design System Palette ──────────────────────────────────────────────
DARK_BG         = "#0f111a"  # Deep canvas background
SURFACE_BG      = "#171a26"  # Card and panel surfaces
SURFACE_ALT     = "#1f2438"  # Inset and elevated container surfaces
INPUT_BG        = "#131622"  # Input fields
BORDER_COLOR    = "#262b3d"  # Subtle modern card borders (replaces harsh outlines)
BORDER_INPUT    = "#2e354e"  # Form control borders
BORDER_FOCUS    = "#6366f1"  # Focus border ring
ACCENT          = "#6366f1"  # Modern Indigo primary
ACCENT_HOVER    = "#4f46e5"  # Indigo hover
ACCENT2         = "#06b6d4"  # Modern Cyan for timestamps & telemetry
SUCCESS_CLR     = "#10b981"  # Emerald Green for Start & Export
SUCCESS_HOVER   = "#059669"
DANGER_CLR      = "#f43f5e"  # Rose Red for Stop & Clear
DANGER_HOVER    = "#e11d48"
BTN_NEUTRAL     = "#202538"  # Secondary ghost buttons
BTN_NEUTRAL_HOVER = "#2b324a"
TEXT_MAIN       = "#f8fafc"  # Crisp high-contrast white text
TEXT_SECONDARY  = "#94a3b8"  # Soft slate text for labels and secondary data
TEXT_MUTED      = "#64748b"  # Muted placeholder and footer text
MOTHER_CLR      = "#f59e0b"  # Warm Amber for Mother role
CHILD_CLR       = "#14b8a6"  # Vibrant Teal for Child role


def ensure_assets():
    base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    assets_dir = os.path.join(base_dir, "assets")
    try:
        os.makedirs(assets_dir, exist_ok=True)
    except Exception:
        import tempfile
        assets_dir = os.path.join(tempfile.gettempdir(), "video_annotator_assets")
        os.makedirs(assets_dir, exist_ok=True)

    up_path = os.path.join(assets_dir, "arrow_up.png")
    dn_path = os.path.join(assets_dir, "arrow_down.png")

    if not os.path.exists(up_path) or not os.path.exists(dn_path):
        from PyQt6.QtGui import QImage, QPainter, QColor, QPolygon
        from PyQt6.QtCore import QPoint

        # Up arrow
        img_up = QImage(16, 16, QImage.Format.Format_ARGB32)
        img_up.fill(QColor(0, 0, 0, 0))
        p = QPainter(img_up)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setBrush(QColor('#94a3b8'))
        p.setPen(QColor(0, 0, 0, 0))
        p.drawPolygon(QPolygon([QPoint(8, 5), QPoint(13, 11), QPoint(3, 11)]))
        p.end()
        img_up.save(up_path, "PNG")

        # Down arrow
        img_dn = QImage(16, 16, QImage.Format.Format_ARGB32)
        img_dn.fill(QColor(0, 0, 0, 0))
        p = QPainter(img_dn)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setBrush(QColor('#94a3b8'))
        p.setPen(QColor(0, 0, 0, 0))
        p.drawPolygon(QPolygon([QPoint(8, 11), QPoint(13, 5), QPoint(3, 5)]))
        p.end()
        img_dn.save(dn_path, "PNG")

    return up_path.replace("\\", "/"), dn_path.replace("\\", "/")

ARROW_UP_PATH, ARROW_DOWN_PATH = ensure_assets()

STYLESHEET = f"""
QMainWindow {{
    background-color: {DARK_BG};
}}
QWidget {{
    color: {TEXT_MAIN};
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial;
    font-size: 13px;
}}
QLabel {{
    background-color: transparent;
    color: {TEXT_MAIN};
}}

/* Card / GroupBox Containers */
QGroupBox {{
    background-color: {SURFACE_BG};
    border: 1px solid {BORDER_COLOR};
    border-radius: 10px;
    margin-top: 22px;
    padding: 16px 14px 14px 14px;
    font-weight: 600;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 14px;
    top: 5px;
    padding: 2px 10px;
    background-color: #202538;
    color: #a5b4fc;
    border: 1px solid #2e354e;
    border-radius: 5px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.3px;
}}

/* Base Buttons */
QPushButton {{
    background-color: {ACCENT};
    color: #ffffff;
    border: 1px solid #4f46e5;
    border-radius: 6px;
    padding: 6px 16px;
    font-weight: 600;
    font-size: 13px;
}}
QPushButton:hover {{
    background-color: {ACCENT_HOVER};
    border-color: #6366f1;
}}
QPushButton:pressed {{
    background-color: #4338ca;
}}
QPushButton:disabled {{
    background-color: #1a1e2c;
    color: #475569;
    border-color: #262b3d;
}}

/* Button Variants */
QPushButton#primary {{
    background-color: {ACCENT};
    border: 1px solid #4f46e5;
    color: #ffffff;
}}
QPushButton#primary:hover {{
    background-color: {ACCENT_HOVER};
}}
QPushButton#success {{
    background-color: {SUCCESS_CLR};
    border: 1px solid #059669;
    color: #ffffff;
}}
QPushButton#success:hover {{
    background-color: {SUCCESS_HOVER};
    border-color: {SUCCESS_CLR};
}}
QPushButton#danger {{
    background-color: {DANGER_CLR};
    border: 1px solid #e11d48;
    color: #ffffff;
}}
QPushButton#danger:hover {{
    background-color: {DANGER_HOVER};
    border-color: {DANGER_CLR};
}}
QPushButton#ghostDanger {{
    background-color: #221820;
    border: 1px solid #5c1d2e;
    color: #fb7185;
}}
QPushButton#ghostDanger:hover {{
    background-color: #381b27;
    border-color: #881337;
    color: #fda4af;
}}
QPushButton#neutral {{
    background-color: {BTN_NEUTRAL};
    border: 1px solid {BORDER_INPUT};
    color: #cbd5e1;
}}
QPushButton#neutral:hover {{
    background-color: {BTN_NEUTRAL_HOVER};
    border-color: #3d4666;
    color: #ffffff;
}}

/* Form Inputs */
QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QTextEdit, QTextBrowser {{
    background-color: {INPUT_BG};
    color: {TEXT_MAIN};
    border: 1px solid {BORDER_INPUT};
    border-radius: 6px;
    padding: 6px 10px;
    selection-background-color: {ACCENT};
    selection-color: #ffffff;
}}
QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus,
QComboBox:focus, QTextEdit:focus, QTextBrowser:focus {{
    border: 1.5px solid {BORDER_FOCUS};
    background-color: #161a29;
}}
QLineEdit[readOnly="true"] {{
    background-color: #11131c;
    color: {TEXT_SECONDARY};
    border-color: #222636;
}}

/* SpinBox Controls & Arrows */
QSpinBox, QDoubleSpinBox {{
    padding-right: 24px;
}}
QSpinBox::up-button, QDoubleSpinBox::up-button {{
    subcontrol-origin: border;
    subcontrol-position: top right;
    width: 22px;
    height: 17px;
    background: #1c2030;
    border-left: 1px solid {BORDER_INPUT};
    border-bottom: 1px solid {BORDER_INPUT};
    border-top-right-radius: 5px;
}}
QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover {{
    background: #2b324a;
}}
QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {{
    image: url("{ARROW_UP_PATH}");
    width: 10px;
    height: 10px;
}}
QSpinBox::down-button, QDoubleSpinBox::down-button {{
    subcontrol-origin: border;
    subcontrol-position: bottom right;
    width: 22px;
    height: 17px;
    background: #1c2030;
    border-left: 1px solid {BORDER_INPUT};
    border-bottom-right-radius: 5px;
}}
QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {{
    background: #2b324a;
}}
QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {{
    image: url("{ARROW_DOWN_PATH}");
    width: 10px;
    height: 10px;
}}

/* ComboBox */
QComboBox {{
    padding-right: 24px;
}}
QComboBox::drop-down {{
    subcontrol-origin: border;
    subcontrol-position: center right;
    width: 22px;
    border: none;
}}
QComboBox::down-arrow {{
    image: url("{ARROW_DOWN_PATH}");
    width: 10px;
    height: 10px;
}}
QComboBox QAbstractItemView {{
    background-color: {SURFACE_BG};
    color: {TEXT_MAIN};
    border: 1px solid #2e354e;
    border-radius: 6px;
    padding: 4px;
    selection-background-color: {ACCENT_HOVER};
    selection-color: #ffffff;
}}

/* Data Table */
QTableWidget {{
    background-color: {INPUT_BG};
    color: {TEXT_MAIN};
    gridline-color: #1c2030;
    border: 1px solid {BORDER_COLOR};
    border-radius: 8px;
    alternate-background-color: #161926;
    selection-background-color: #312e81;
    selection-color: #ffffff;
}}
QHeaderView::section {{
    background-color: #1c2030;
    color: {TEXT_SECONDARY};
    border: none;
    border-bottom: 2px solid {BORDER_COLOR};
    border-right: 1px solid #1c2030;
    padding: 8px;
    font-weight: 700;
    font-size: 11px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}}
QTableWidget QTableCornerButton::section {{
    background-color: #1c2030;
    border: none;
}}

/* Scrollbars */
QScrollBar:vertical {{
    background: {INPUT_BG};
    width: 8px;
    margin: 0;
    border-radius: 4px;
}}
QScrollBar::handle:vertical {{
    background: #2b324a;
    min-height: 24px;
    border-radius: 4px;
}}
QScrollBar::handle:vertical:hover {{
    background: #475569;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}
QScrollBar:horizontal {{
    background: {INPUT_BG};
    height: 8px;
    margin: 0;
    border-radius: 4px;
}}
QScrollBar::handle:horizontal {{
    background: #2b324a;
    min-width: 24px;
    border-radius: 4px;
}}
QScrollBar::handle:horizontal:hover {{
    background: #475569;
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0px;
}}

/* Splitter */
QSplitter::handle:horizontal {{
    background-color: transparent;
    width: 16px;
}}
QSplitter::handle:hover {{
    background-color: #1a1e2d;
}}
"""


def fmt_time(ms: int) -> str:
    s = ms // 1000
    return str(timedelta(seconds=s))


class ClickableVideoWidget(QVideoWidget):
    doubleClicked = pyqtSignal()

    def mouseDoubleClickEvent(self, event):
        self.doubleClicked.emit()
        super().mouseDoubleClickEvent(event)


class FloatingHUD(QWidget):
    """
    Independent top-level translucent floating window for Full Screen mode.
    Stays on top of native macOS/Windows video layers and can be dragged by users.
    """
    def __init__(self, main_win):
        super().__init__(main_win, Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.main_win = main_win
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._drag_pos = None

        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(10, 10, 10, 10)

        # Card container with semi-transparent glassmorphic styling
        self.card = QFrame()
        self.card.setObjectName("hudCard")
        self.card.setStyleSheet(f"""
            QFrame#hudCard {{
                background-color: rgba(15, 17, 26, 0.95);
                border: 1px solid #3b4261;
                border-radius: 14px;
            }}
        """)
        # Drop shadow for depth and separation from video
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(28)
        shadow.setColor(QColor(0, 0, 0, 200))
        shadow.setOffset(0, 8)
        self.card.setGraphicsEffect(shadow)

        card_lay = QVBoxLayout(self.card)
        card_lay.setContentsMargins(16, 14, 16, 16)
        card_lay.setSpacing(10)

        # Top Header Bar (Draggable handle + badges + exit button)
        hdr = QHBoxLayout()
        hdr.setSpacing(10)

        drag_icon = QLabel("⠿ Drag HUD")
        drag_icon.setStyleSheet("color: #64748b; font-size: 11px; font-weight: 700; padding: 2px 6px;")
        hdr.addWidget(drag_icon)

        title_lbl = QLabel("🎬 Fullscreen Annotation")
        title_lbl.setStyleSheet(f"color: {ACCENT2}; font-weight: 700; font-size: 12px;")
        hdr.addWidget(title_lbl)

        self.hud_label_combo = QComboBox()
        self.hud_label_combo.addItems(["Mother", "Child"])
        self.hud_label_combo.setCursor(Qt.CursorShape.PointingHandCursor)
        self.hud_label_combo.setToolTip("Change participant label (Mother / Child)")
        self.hud_label_combo.currentTextChanged.connect(self.main_win._on_hud_label_change)
        hdr.addWidget(self.hud_label_combo)

        self.hud_time_lbl = QLabel("00:00:00 / 00:00:00")
        self.hud_time_lbl.setStyleSheet(f"background: #131622; color: {TEXT_MAIN}; font-family: 'Courier New', monospace; font-weight: bold; font-size: 11px; padding: 4px 10px; border-radius: 10px; border: 1px solid {BORDER_INPUT};")
        hdr.addWidget(self.hud_time_lbl)

        self.hud_step_lbl = QLabel("Step — / —")
        self.hud_step_lbl.setStyleSheet(f"background: #131622; color: {ACCENT2}; font-weight: bold; font-size: 11px; padding: 4px 10px; border-radius: 10px; border: 1px solid {BORDER_INPUT};")
        hdr.addWidget(self.hud_step_lbl)

        hdr.addStretch()

        btn_exit = QPushButton("✕ Exit Full Screen")
        btn_exit.setObjectName("ghostDanger")
        btn_exit.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_exit.setMinimumHeight(30)
        btn_exit.clicked.connect(self.main_win._toggle_fullscreen)
        hdr.addWidget(btn_exit)

        card_lay.addLayout(hdr)

        # Question prompt display
        self.hud_q_counter = QLabel("Question — / —")
        self.hud_q_counter.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.hud_q_counter.setStyleSheet("color: #a5b4fc; background: rgba(99, 102, 241, 0.15); border: 1px solid #4338ca; border-radius: 10px; padding: 2px 10px;")
        card_lay.addWidget(self.hud_q_counter)

        self.hud_q_text = QLabel("(no active session)")
        self.hud_q_text.setWordWrap(True)
        self.hud_q_text.setFont(QFont("Segoe UI", 12, QFont.Weight.DemiBold))
        self.hud_q_text.setStyleSheet(f"color: {TEXT_MAIN}; padding: 10px; background: {INPUT_BG}; border-radius: 8px; border: 1px solid {BORDER_INPUT};")
        card_lay.addWidget(self.hud_q_text)

        # Answer text input
        self.hud_ans_input = QTextEdit()
        self.hud_ans_input.setPlaceholderText("Type your answer here… (Ctrl+Enter or Cmd+Enter to submit)")
        self.hud_ans_input.setMaximumHeight(75)
        self.hud_ans_input.installEventFilter(self.main_win)
        self.hud_ans_input.setStyleSheet(f"background: {INPUT_BG}; color: {TEXT_MAIN}; border: 1.5px solid {BORDER_INPUT}; border-radius: 8px; padding: 8px;")
        card_lay.addWidget(self.hud_ans_input)

        # Action Buttons (Next / Skip) — Equal size (50% / 50%)
        h_btn_row = QHBoxLayout()
        h_btn_row.setSpacing(10)

        self.hud_btn_next = QPushButton("Next Question  ›")
        self.hud_btn_next.setObjectName("primary")
        self.hud_btn_next.setMinimumHeight(40)
        self.hud_btn_next.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.hud_btn_next.setCursor(Qt.CursorShape.PointingHandCursor)
        self.hud_btn_next.clicked.connect(self.main_win._next_question)
        self.hud_btn_next.setEnabled(False)

        self.hud_btn_skip = QPushButton("Skip Question")
        self.hud_btn_skip.setObjectName("neutral")
        self.hud_btn_skip.setMinimumHeight(40)
        self.hud_btn_skip.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.hud_btn_skip.setCursor(Qt.CursorShape.PointingHandCursor)
        self.hud_btn_skip.clicked.connect(self.main_win._skip_question)
        self.hud_btn_skip.setEnabled(False)

        h_btn_row.addWidget(self.hud_btn_next, 1)
        h_btn_row.addWidget(self.hud_btn_skip, 1)
        card_lay.addLayout(h_btn_row)

        root.addWidget(self.card)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._drag_pos is not None and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_pos = None
        event.accept()


class VideoAnnotator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Video Annotation Tool v{__version__} [GPL-3.0]")
        self.resize(1420, 890)

        self.video_path     = ""
        self.questions      = []
        self.records        = []
        self.current_q      = 0
        self.answers_buf    = {}
        self.step_ms        = 1000
        self.range_start    = 0
        self.range_end      = 0
        self.label          = "Mother"
        self.processing     = False
        self.waiting_ans    = False
        self.current_pos    = 0
        self.total_steps    = 0
        self.is_fullscreen  = False
        self.preset_btns    = {}

        # Safely pre-initialize input widgets before UI construction
        self.ans_input      = None
        self.btn_next_q     = None
        self.btn_skip_q     = None
        self.floating_hud   = None

        self._build_ui()
        self.floating_hud = FloatingHUD(self)
        self._update_hud_combo_style(self.label)
        self.setStyleSheet(STYLESHEET)

    # ── UI ─────────────────────────────────────────────────────────────────────
    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setSpacing(8)
        root.setContentsMargins(12, 10, 12, 12)

        # Top Bar
        self.top_bar_widget = QWidget()
        top_bar = QHBoxLayout(self.top_bar_widget)
        top_bar.setContentsMargins(4, 2, 4, 6)

        title_lbl = QLabel("🎬 VIDEO ANNOTATOR")
        title_lbl.setFont(QFont("Segoe UI", 13, QFont.Weight.ExtraBold))
        title_lbl.setStyleSheet(f"color: {TEXT_MAIN}; letter-spacing: 0.5px;")

        ver_lbl = QLabel(f"v{__version__} • GPL-3.0")
        ver_lbl.setStyleSheet(f"background: #1c2030; color: {TEXT_MUTED}; font-size: 11px; font-weight: 600; padding: 3px 8px; border-radius: 6px; border: 1px solid {BORDER_COLOR};")

        top_bar.addWidget(title_lbl)
        top_bar.addSpacing(8)
        top_bar.addWidget(ver_lbl)
        top_bar.addStretch()

        btn_manual = QPushButton("📖  User Manual")
        btn_manual.setObjectName("neutral")
        btn_manual.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_manual.clicked.connect(self._show_manual)
        top_bar.addWidget(btn_manual)

        btn_about = QPushButton("⚖️  About / License")
        btn_about.setObjectName("neutral")
        btn_about.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_about.clicked.connect(self._show_about)
        top_bar.addWidget(btn_about)

        root.addWidget(self.top_bar_widget)

        # Resizable Splitter with distinct gap between panels
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.setHandleWidth(16)
        self.splitter.setChildrenCollapsible(False)
        root.addWidget(self.splitter, stretch=1)
        self.splitter.addWidget(self._build_left())
        self.right_panel = self._build_right()
        self.splitter.addWidget(self.right_panel)
        self.splitter.setSizes([740, 680])

    def _build_left(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setSpacing(8)
        lay.setContentsMargins(0, 0, 4, 0)

        # Video Widget (Resizable, Expanding, Double-click to Fullscreen)
        self.video_widget = ClickableVideoWidget()
        self.video_widget.setMinimumHeight(240)
        self.video_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.video_widget.setStyleSheet(f"background: #000000; border: 1px solid {BORDER_COLOR}; border-radius: 8px;")
        self.video_widget.doubleClicked.connect(self._toggle_fullscreen)
        lay.addWidget(self.video_widget, stretch=1)

        # Media Player bindings
        self.player = QMediaPlayer()
        self.audio  = QAudioOutput()
        self.player.setAudioOutput(self.audio)
        self.player.setVideoOutput(self.video_widget)
        self.player.positionChanged.connect(self._on_position_changed)
        self.player.durationChanged.connect(self._on_duration_changed)

        # Video Toolbar: Timestamp & Fullscreen Button
        self.video_control_bar = QWidget()
        v_bar = QHBoxLayout(self.video_control_bar)
        v_bar.setContentsMargins(2, 4, 2, 4)

        self.time_lbl = QLabel("00:00:00 / 00:00:00")
        self.time_lbl.setFont(QFont("Courier New", 12, QFont.Weight.Bold))
        self.time_lbl.setStyleSheet(f"color: {ACCENT2}; background: #131622; padding: 5px 12px; border-radius: 6px; border: 1px solid {BORDER_COLOR};")
        v_bar.addWidget(self.time_lbl)

        v_bar.addStretch()

        self.btn_fs = QPushButton("⛶  Full Screen")
        self.btn_fs.setObjectName("neutral")
        self.btn_fs.setToolTip("Toggle Full Screen (F11 or double-click video)")
        self.btn_fs.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_fs.clicked.connect(self._toggle_fullscreen)
        v_bar.addWidget(self.btn_fs)

        lay.addWidget(self.video_control_bar)

        # Left Controls container (hidden in fullscreen)
        self.left_controls_widget = QWidget()
        cl = QVBoxLayout(self.left_controls_widget)
        cl.setSpacing(8)
        cl.setContentsMargins(0, 0, 0, 0)

        # File loading group with Grid Layout for uniform alignment
        fg = QGroupBox("Load Files")
        fl = QGridLayout(fg)
        fl.setContentsMargins(14, 14, 14, 14)
        fl.setHorizontalSpacing(10)
        fl.setVerticalSpacing(8)

        lbl_vid = QLabel("Video File:")
        lbl_vid.setFixedWidth(95)
        lbl_vid.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        lbl_vid.setStyleSheet(f"color: {TEXT_SECONDARY}; font-weight: 600;")
        self.video_path_lbl = QLineEdit()
        self.video_path_lbl.setPlaceholderText("Select video file to annotate…")
        self.video_path_lbl.setReadOnly(True)
        self.video_path_lbl.setFixedHeight(36)
        btn_vid = QPushButton("Browse Video")
        btn_vid.setObjectName("neutral")
        btn_vid.setFixedWidth(120)
        btn_vid.setFixedHeight(36)
        btn_vid.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_vid.clicked.connect(self._browse_video)

        fl.addWidget(lbl_vid, 0, 0)
        fl.addWidget(self.video_path_lbl, 0, 1)
        fl.addWidget(btn_vid, 0, 2)

        lbl_txt = QLabel("Questions:")
        lbl_txt.setFixedWidth(95)
        lbl_txt.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        lbl_txt.setStyleSheet(f"color: {TEXT_SECONDARY}; font-weight: 600;")
        self.txt_path_lbl = QLineEdit()
        self.txt_path_lbl.setPlaceholderText("Select questions file (.txt)…")
        self.txt_path_lbl.setReadOnly(True)
        self.txt_path_lbl.setFixedHeight(36)
        btn_txt = QPushButton("Browse Questions")
        btn_txt.setObjectName("neutral")
        btn_txt.setFixedWidth(120)
        btn_txt.setFixedHeight(36)
        btn_txt.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_txt.clicked.connect(self._browse_txt)

        fl.addWidget(lbl_txt, 1, 0)
        fl.addWidget(self.txt_path_lbl, 1, 1)
        fl.addWidget(btn_txt, 1, 2)
        cl.addWidget(fg)

        # Session Settings group with unified 2-column Grid Layout
        cg = QGroupBox("Session Settings")
        cgl = QGridLayout(cg)
        cgl.setContentsMargins(14, 14, 14, 14)
        cgl.setHorizontalSpacing(10)
        cgl.setVerticalSpacing(10)

        # Row 0: Time Range (Start and End equal width, paired side-by-side)
        lbl_range = QLabel("Time Range:")
        lbl_range.setFixedWidth(95)
        lbl_range.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        lbl_range.setStyleSheet(f"color: {TEXT_SECONDARY}; font-weight: 600;")

        range_container = QWidget()
        range_container.setStyleSheet("background: transparent;")
        range_layout = QHBoxLayout(range_container)
        range_layout.setContentsMargins(0, 0, 0, 0)
        range_layout.setSpacing(8)

        lbl_start_sub = QLabel("Start (s):")
        lbl_start_sub.setStyleSheet(f"color: {TEXT_SECONDARY}; font-weight: 500;")
        self.start_spin = QSpinBox()
        self.start_spin.setRange(0, 999999)
        self.start_spin.setFixedWidth(110)
        self.start_spin.setFixedHeight(36)

        lbl_end_sub = QLabel("End (s):")
        lbl_end_sub.setStyleSheet(f"color: {TEXT_SECONDARY}; font-weight: 500;")
        self.end_spin = QSpinBox()
        self.end_spin.setRange(0, 999999)
        self.end_spin.setValue(60)
        self.end_spin.setFixedWidth(110)
        self.end_spin.setFixedHeight(36)

        range_layout.addWidget(lbl_start_sub)
        range_layout.addWidget(self.start_spin)
        range_layout.addSpacing(16)
        range_layout.addWidget(lbl_end_sub)
        range_layout.addWidget(self.end_spin)
        range_layout.addStretch()

        cgl.addWidget(lbl_range, 0, 0)
        cgl.addWidget(range_container, 0, 1)

        # Row 1: Step Presets
        lbl_presets = QLabel("Step Presets:")
        lbl_presets.setFixedWidth(95)
        lbl_presets.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        lbl_presets.setStyleSheet(f"color: {TEXT_SECONDARY}; font-weight: 600;")

        preset_container = QWidget()
        preset_container.setStyleSheet("background: transparent;")
        preset_layout = QHBoxLayout(preset_container)
        preset_layout.setContentsMargins(0, 0, 0, 0)
        preset_layout.setSpacing(6)

        self.preset_btns = {}
        for val in [0.5, 1.0, 5.0, 10.0]:
            label = f"{val:g}s"
            btn = QPushButton(label)
            btn.setObjectName("neutral")
            btn.setFixedHeight(32)
            btn.setMinimumWidth(54)
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, v=val: self._on_preset_clicked(v))
            preset_layout.addWidget(btn)
            self.preset_btns[val] = btn
        preset_layout.addStretch()

        cgl.addWidget(lbl_presets, 1, 0)
        cgl.addWidget(preset_container, 1, 1)

        # Row 2: Custom Step Size & Participant Label
        lbl_step = QLabel("Step & Role:")
        lbl_step.setFixedWidth(95)
        lbl_step.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        lbl_step.setStyleSheet(f"color: {TEXT_SECONDARY}; font-weight: 600;")

        step_role_container = QWidget()
        step_role_container.setStyleSheet("background: transparent;")
        step_role_layout = QHBoxLayout(step_role_container)
        step_role_layout.setContentsMargins(0, 0, 0, 0)
        step_role_layout.setSpacing(8)

        lbl_step_sub = QLabel("Step (s):")
        lbl_step_sub.setStyleSheet(f"color: {TEXT_SECONDARY}; font-weight: 500;")
        self.step_spin = QDoubleSpinBox()
        self.step_spin.setRange(0.1, 300)
        self.step_spin.setValue(1.0)
        self.step_spin.setSingleStep(0.5)
        self.step_spin.setFixedWidth(110)
        self.step_spin.setFixedHeight(36)
        self.step_spin.valueChanged.connect(self._on_step_value_changed)

        lbl_role_sub = QLabel("Role:")
        lbl_role_sub.setStyleSheet(f"color: {TEXT_SECONDARY}; font-weight: 500;")

        self.label_combo = QComboBox()
        self.label_combo.addItems(["Mother", "Child"])
        self.label_combo.setFixedWidth(110)
        self.label_combo.setFixedHeight(36)
        self.label_combo.setCursor(Qt.CursorShape.PointingHandCursor)
        self.label_combo.currentTextChanged.connect(self._on_label_change)

        self.badge = QLabel("● Mother")
        self.badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.badge.setFixedHeight(36)
        self.badge.setStyleSheet(f"background: rgba(245, 158, 11, 0.15); color: {MOTHER_CLR}; border: 1px solid rgba(245, 158, 11, 0.35); border-radius: 8px; padding: 4px 14px; font-weight: 700;")

        step_role_layout.addWidget(lbl_step_sub)
        step_role_layout.addWidget(self.step_spin)
        step_role_layout.addSpacing(16)
        step_role_layout.addWidget(lbl_role_sub)
        step_role_layout.addWidget(self.label_combo)
        step_role_layout.addWidget(self.badge)
        step_role_layout.addStretch()

        cgl.addWidget(lbl_step, 2, 0)
        cgl.addWidget(step_role_container, 2, 1)

        cl.addWidget(cg)

        # Action buttons: Start / Stop (Symmetric size: 50% / 50%, height 44px)
        br = QHBoxLayout()
        br.setSpacing(10)
        self.btn_start = QPushButton("▶  Start Processing")
        self.btn_start.setObjectName("success")
        self.btn_start.setMinimumHeight(44)
        self.btn_start.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.btn_start.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_start.clicked.connect(self._start_processing)

        self.btn_stop = QPushButton("■  Stop Processing")
        self.btn_stop.setObjectName("danger")
        self.btn_stop.setMinimumHeight(44)
        self.btn_stop.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.btn_stop.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_stop.setEnabled(False)
        self.btn_stop.clicked.connect(self._stop_processing)

        br.addWidget(self.btn_start, 1)
        br.addWidget(self.btn_stop, 1)
        cl.addLayout(br)

        self.status_lbl = QLabel("● Ready")
        self.status_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_lbl.setStyleSheet(f"color: {ACCENT2}; background: #131622; padding: 6px; border-radius: 6px; border: 1px solid {BORDER_COLOR}; font-weight: 500;")
        cl.addWidget(self.status_lbl)

        lay.addWidget(self.left_controls_widget)

        # Initialize preset button highlight
        self._on_step_value_changed(1.0)
        return w

    def _build_right(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setSpacing(10)
        lay.setContentsMargins(4, 0, 0, 0)

        qa_grp = QGroupBox("Current Question Prompt")
        qg = QVBoxLayout(qa_grp)
        qg.setContentsMargins(14, 14, 14, 14)
        qg.setSpacing(10)

        # Header row in question card
        q_hdr = QHBoxLayout()
        self.q_counter = QLabel("Question — / —")
        self.q_counter.setStyleSheet("background: rgba(99, 102, 241, 0.15); color: #a5b4fc; border: 1px solid #4338ca; border-radius: 10px; padding: 3px 10px; font-weight: 700; font-size: 11px;")
        q_hdr.addWidget(self.q_counter)

        q_hint = QLabel("Press Ctrl+Enter / Cmd+Enter to advance")
        q_hint.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 11px;")
        q_hdr.addStretch()
        q_hdr.addWidget(q_hint)
        qg.addLayout(q_hdr)

        self.q_text = QLabel("(no active session — click 'Start Processing' to begin)")
        self.q_text.setWordWrap(True)
        self.q_text.setFont(QFont("Segoe UI", 12, QFont.Weight.DemiBold))
        self.q_text.setStyleSheet(f"color: {TEXT_MAIN}; padding: 12px; background: {INPUT_BG}; border: 1px solid {BORDER_INPUT}; border-radius: 8px;")
        self.q_text.setMinimumHeight(60)
        qg.addWidget(self.q_text)

        self.ans_input = QTextEdit()
        self.ans_input.setPlaceholderText("Type observation or answer here…")
        self.ans_input.setMaximumHeight(85)
        self.ans_input.setEnabled(False)
        self.ans_input.installEventFilter(self)
        qg.addWidget(self.ans_input)

        # Question Action buttons: Next / Skip (Equal size: 50% / 50%, height 40px)
        ab = QHBoxLayout()
        ab.setSpacing(10)
        self.btn_next_q = QPushButton("Next Question  ›")
        self.btn_next_q.setObjectName("primary")
        self.btn_next_q.setMinimumHeight(40)
        self.btn_next_q.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.btn_next_q.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_next_q.clicked.connect(self._next_question)
        self.btn_next_q.setEnabled(False)

        self.btn_skip_q = QPushButton("Skip Question")
        self.btn_skip_q.setObjectName("neutral")
        self.btn_skip_q.setMinimumHeight(40)
        self.btn_skip_q.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.btn_skip_q.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_skip_q.clicked.connect(self._skip_question)
        self.btn_skip_q.setEnabled(False)

        ab.addWidget(self.btn_next_q, 1)
        ab.addWidget(self.btn_skip_q, 1)
        qg.addLayout(ab)
        lay.addWidget(qa_grp)

        tbl_grp = QGroupBox("Annotation Records")
        tg = QVBoxLayout(tbl_grp)
        tg.setContentsMargins(14, 14, 14, 14)
        tg.setSpacing(10)

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["Video", "Label", "Timestamp", "Step #", "Question", "Answer"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setDefaultSectionSize(32)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        tg.addWidget(self.table)

        # Table Action buttons: Export / Clear (Equal size: 50% / 50%, height 40px)
        tb = QHBoxLayout()
        tb.setSpacing(10)
        self.btn_export = QPushButton("⬇  Export to Excel")
        self.btn_export.setObjectName("success")
        self.btn_export.setMinimumHeight(40)
        self.btn_export.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.btn_export.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_export.clicked.connect(self._export_excel)
        self.btn_export.setEnabled(False)

        btn_clear = QPushButton("🗑  Clear Table")
        btn_clear.setObjectName("ghostDanger")
        btn_clear.setMinimumHeight(40)
        btn_clear.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        btn_clear.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_clear.clicked.connect(self._clear_table)

        tb.addWidget(self.btn_export, 1)
        tb.addWidget(btn_clear, 1)
        tg.addLayout(tb)
        lay.addWidget(tbl_grp, stretch=1)
        return w

    # ── Presets Handling ───────────────────────────────────────────────────────
    def _on_preset_clicked(self, val: float):
        self.step_spin.setValue(val)

    def _on_step_value_changed(self, val: float):
        for p_val, btn in self.preset_btns.items():
            if abs(p_val - val) < 0.001:
                btn.setChecked(True)
                btn.setStyleSheet(f"background-color: {ACCENT}; color: #ffffff; font-weight: bold; border: 1px solid #818cf8; border-radius: 6px;")
            else:
                btn.setChecked(False)
                btn.setStyleSheet(f"background-color: #1c2030; color: {TEXT_SECONDARY}; font-weight: 500; border: 1px solid #2b324a; border-radius: 6px;")

    # ── Full Screen Handling ───────────────────────────────────────────────────
    def _toggle_fullscreen(self):
        if self.is_fullscreen:
            # Return to normal windowed view
            self.is_fullscreen = False
            if self.floating_hud:
                self.floating_hud.hide()
            self.top_bar_widget.show()
            self.left_controls_widget.show()
            self.video_control_bar.show()
            self.right_panel.show()
            self.btn_fs.setText("⛶ Full Screen")
            self.showNormal()
        else:
            # Enter full screen mode with floating HUD
            self.is_fullscreen = True
            self.top_bar_widget.hide()
            self.left_controls_widget.hide()
            self.video_control_bar.hide()
            self.right_panel.hide()
            self.btn_fs.setText("✕ Exit Full Screen")
            self.showFullScreen()

            # Position floating HUD near the bottom of current screen
            if self.floating_hud:
                screen_geo = self.screen().geometry()
                hud_w = min(780, screen_geo.width() - 40)
                hud_h = 300
                hud_x = screen_geo.x() + max(20, (screen_geo.width() - hud_w) // 2)
                hud_y = screen_geo.y() + max(20, screen_geo.height() - hud_h - 40)
                self.floating_hud.setGeometry(hud_x, hud_y, hud_w, hud_h)
                self.floating_hud.show()
                self.floating_hud.raise_()
                self.floating_hud.activateWindow()

                if self.waiting_ans:
                    self.floating_hud.hud_ans_input.setFocus()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape and self.is_fullscreen:
            self._toggle_fullscreen()
            event.accept()
            return
        if event.key() == Qt.Key.Key_F11:
            self._toggle_fullscreen()
            event.accept()
            return
        super().keyPressEvent(event)

    def closeEvent(self, event):
        if hasattr(self, 'floating_hud') and self.floating_hud:
            self.floating_hud.close()
        super().closeEvent(event)

    # ── Event Filter (Keyboard Shortcuts) ──────────────────────────────────────
    def eventFilter(self, obj, event):
        targets = []
        if getattr(self, "ans_input", None) is not None:
            targets.append(self.ans_input)
        if hasattr(self, "floating_hud") and self.floating_hud and getattr(self.floating_hud, "hud_ans_input", None) is not None:
            targets.append(self.floating_hud.hud_ans_input)

        if targets and (obj in targets) and event.type() == QEvent.Type.KeyPress:
            if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                if event.modifiers() & (Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.MetaModifier):
                    btn_main = getattr(self, "btn_next_q", None)
                    btn_hud = getattr(self.floating_hud, "hud_btn_next", None) if hasattr(self, "floating_hud") and self.floating_hud else None
                    if (btn_main and btn_main.isEnabled()) or (btn_hud and btn_hud.isEnabled()):
                        self._next_question()
                        return True
            elif event.key() == Qt.Key.Key_Escape and self.is_fullscreen:
                self._toggle_fullscreen()
                return True
        return super().eventFilter(obj, event)

    # ── In-App Help & Dialogs ──────────────────────────────────────────────────
    def _show_manual(self):
        base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        manual_path = os.path.join(base_dir, "USER_MANUAL.md")
        if not os.path.exists(manual_path):
            manual_path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "USER_MANUAL.md")

        content = ""
        if os.path.exists(manual_path):
            try:
                with open(manual_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                content = f"Error reading manual: {e}"
        else:
            content = (
                "# Video Annotation Tool — Quick Guide\n\n"
                "### Workflow:\n"
                "1. **Load Video & Questions**: Browse to select a video and a `.txt` file with one question per line.\n"
                "2. **Configure Range & Step**: Set start time, end time, and step interval (e.g. 0.5s, 1s, 5s, 10s presets).\n"
                "3. **Choose Label**: Select participant role (Mother or Child).\n"
                "4. **Click Start Processing**: Step through video. Use Full Screen (F11) with floating HUD for immersion.\n"
                "5. **Export to Excel**: Once finished, click 'Export to Excel' to save formatted `.xlsx`.\n"
            )

        dlg = QDialog(self)
        dlg.setWindowTitle("User Manual — Video Annotation Tool")
        dlg.resize(900, 700)
        d_lay = QVBoxLayout(dlg)
        d_lay.setSpacing(10)
        d_lay.setContentsMargins(12, 12, 12, 12)

        browser = QTextBrowser()
        browser.setOpenExternalLinks(True)
        browser.setMarkdown(content)
        browser.setStyleSheet(f"background: {INPUT_BG}; color: {TEXT_MAIN}; border: 1px solid {BORDER_COLOR}; border-radius: 8px; padding: 14px;")
        d_lay.addWidget(browser)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_close = QPushButton("Close")
        btn_close.setObjectName("neutral")
        btn_close.setFixedWidth(100)
        btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_close.clicked.connect(dlg.accept)
        btn_row.addWidget(btn_close)
        d_lay.addLayout(btn_row)

        dlg.exec()

    def _show_about(self):
        about_text = (
            f"<h3>🎬 Video Annotation Tool v{__version__}</h3>"
            "<p>A modern desktop video observation and interval annotation system.</p>"
            "<p><b>License:</b> GNU General Public License v3.0 (GPL-3.0)<br>"
            "This is free software; you are free to change and redistribute it under GPLv3.<br>"
            "There is NO WARRANTY, to the extent permitted by law.</p>"
            "<p>Full license terms are available in the bundled <code>LICENSE</code> file or at:<br>"
            f"<a href='https://www.gnu.org/licenses/gpl-3.0.html' style='color:{ACCENT2};'>https://www.gnu.org/licenses/gpl-3.0.html</a></p>"
        )
        QMessageBox.about(self, "About Video Annotation Tool", about_text)

    # ── File browsing ──────────────────────────────────────────────────────────
    def _browse_video(self):
        path, _ = QFileDialog.getOpenFileName(self,"Open Video","","Video Files (*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm)")
        if path:
            self.video_path = path
            self.video_path_lbl.setText(path)
            self.player.setSource(QUrl.fromLocalFile(path))
            self.player.pause()
            self._set_status(f"Loaded: {os.path.basename(path)}")

    def _browse_txt(self):
        path, _ = QFileDialog.getOpenFileName(self,"Open Questions File","","Text Files (*.txt)")
        if path:
            with open(path,"r",encoding="utf-8") as f:
                self.questions = [l.strip() for l in f if l.strip()]
            self.txt_path_lbl.setText(path)
            self._set_status(f"Loaded {len(self.questions)} questions.")

    def _on_label_change(self, text):
        self.label = text
        is_mother = text == "Mother"
        clr = MOTHER_CLR if is_mother else CHILD_CLR
        bg_clr = "rgba(245, 158, 11, 0.15)" if is_mother else "rgba(20, 184, 166, 0.15)"
        border_clr = "rgba(245, 158, 11, 0.35)" if is_mother else "rgba(20, 184, 166, 0.35)"
        self.badge.setText(f"● {text}")
        self.badge.setStyleSheet(f"background: {bg_clr}; color: {clr}; border: 1px solid {border_clr}; border-radius: 8px; padding: 4px 12px; font-weight: 700;")
        if hasattr(self, 'floating_hud') and self.floating_hud and hasattr(self.floating_hud, 'hud_label_combo'):
            if self.floating_hud.hud_label_combo.currentText() != text:
                self.floating_hud.hud_label_combo.blockSignals(True)
                self.floating_hud.hud_label_combo.setCurrentText(text)
                self.floating_hud.hud_label_combo.blockSignals(False)
            self._update_hud_combo_style(text)

    def _on_hud_label_change(self, text):
        self.label_combo.blockSignals(True)
        self.label_combo.setCurrentText(text)
        self.label_combo.blockSignals(False)
        self._on_label_change(text)

    def _update_hud_combo_style(self, text):
        if hasattr(self, 'floating_hud') and self.floating_hud and hasattr(self.floating_hud, 'hud_label_combo'):
            is_mother = text == "Mother"
            clr = MOTHER_CLR if is_mother else CHILD_CLR
            bg_clr = "rgba(245, 158, 11, 0.15)" if is_mother else "rgba(20, 184, 166, 0.15)"
            border_clr = "rgba(245, 158, 11, 0.35)" if is_mother else "rgba(20, 184, 166, 0.35)"
            self.floating_hud.hud_label_combo.setStyleSheet(f"""
                QComboBox {{
                    background-color: {bg_clr};
                    color: {clr};
                    font-weight: 700;
                    border: 1px solid {border_clr};
                    border-radius: 8px;
                    padding: 3px 8px;
                    min-width: 80px;
                }}
                QComboBox::drop-down {{
                    border: none;
                    width: 14px;
                }}
                QComboBox QAbstractItemView {{
                    background-color: {SURFACE_BG};
                    color: {TEXT_MAIN};
                    selection-background-color: {ACCENT_HOVER};
                }}
            """)

    def _on_position_changed(self, pos):
        dur = self.player.duration() or 0
        t_str = f"{fmt_time(pos)} / {fmt_time(dur)}"
        self.time_lbl.setText(t_str)
        if hasattr(self, 'floating_hud') and self.floating_hud:
            self.floating_hud.hud_time_lbl.setText(t_str)

    def _on_duration_changed(self, dur):
        if dur:
            self.end_spin.setValue(dur // 1000)

    # ── Processing ─────────────────────────────────────────────────────────────
    def _start_processing(self):
        if not self.video_path:
            QMessageBox.warning(self,"No Video","Please load a video file first."); return
        if not self.questions:
            QMessageBox.warning(self,"No Questions","Please load a questions file first."); return
        self.range_start = self.start_spin.value() * 1000
        self.range_end   = self.end_spin.value()   * 1000
        self.step_ms     = int(self.step_spin.value() * 1000)
        self.label       = self.label_combo.currentText()
        if self.range_end <= self.range_start:
            QMessageBox.warning(self,"Invalid Range","End time must be greater than start time."); return
        self.processing   = True
        self.total_steps  = max(1,(self.range_end - self.range_start) // self.step_ms)
        self.current_pos  = self.range_start
        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.player.setPosition(self.current_pos)
        self.player.play()
        QTimer.singleShot(500, self._begin_step)

    def _begin_step(self):
        if not self.processing: return
        self.player.pause()
        self.current_q   = 0
        self.answers_buf = {}
        step_num = (self.current_pos - self.range_start) // self.step_ms + 1
        s_text = f"Step {step_num} / {self.total_steps}  •  {fmt_time(self.current_pos)}"
        self._set_status(s_text)
        if hasattr(self, 'floating_hud') and self.floating_hud:
            self.floating_hud.hud_step_lbl.setText(f"Step {step_num} / {self.total_steps}")
        self._show_question()

    def _show_question(self):
        if self.current_q >= len(self.questions):
            self._save_step_records()
            self._advance_step()
            return

        counter_text = f"Question {self.current_q+1} / {len(self.questions)}"
        q_text = self.questions[self.current_q]

        # Update standard panel
        self.q_counter.setText(counter_text)
        self.q_text.setText(q_text)
        self.ans_input.clear()
        self.ans_input.setEnabled(True)
        self.btn_next_q.setEnabled(True)
        self.btn_skip_q.setEnabled(True)

        # Update floating HUD
        if hasattr(self, 'floating_hud') and self.floating_hud:
            self.floating_hud.hud_q_counter.setText(counter_text)
            self.floating_hud.hud_q_text.setText(q_text)
            self.floating_hud.hud_ans_input.clear()
            self.floating_hud.hud_ans_input.setEnabled(True)
            self.floating_hud.hud_btn_next.setEnabled(True)
            self.floating_hud.hud_btn_skip.setEnabled(True)

        self.waiting_ans = True
        if self.is_fullscreen and hasattr(self, 'floating_hud') and self.floating_hud:
            self.floating_hud.hud_ans_input.setFocus()
        else:
            self.ans_input.setFocus()

    def _next_question(self):
        if not self.waiting_ans: return
        # Extract response from active input
        if self.is_fullscreen and hasattr(self, 'floating_hud') and self.floating_hud:
            ans = self.floating_hud.hud_ans_input.toPlainText().strip()
        else:
            ans = self.ans_input.toPlainText().strip()

        self.answers_buf[self.current_q] = ans
        self.current_q += 1

        self.ans_input.setEnabled(False); self.btn_next_q.setEnabled(False); self.btn_skip_q.setEnabled(False)
        if hasattr(self, 'floating_hud') and self.floating_hud:
            self.floating_hud.hud_ans_input.setEnabled(False)
            self.floating_hud.hud_btn_next.setEnabled(False)
            self.floating_hud.hud_btn_skip.setEnabled(False)
        self.waiting_ans = False
        self._show_question()

    def _skip_question(self):
        self.answers_buf[self.current_q] = ""
        self.current_q += 1

        self.ans_input.setEnabled(False); self.btn_next_q.setEnabled(False); self.btn_skip_q.setEnabled(False)
        if hasattr(self, 'floating_hud') and self.floating_hud:
            self.floating_hud.hud_ans_input.setEnabled(False)
            self.floating_hud.hud_btn_next.setEnabled(False)
            self.floating_hud.hud_btn_skip.setEnabled(False)
        self.waiting_ans = False
        self._show_question()

    def _save_step_records(self):
        ts = fmt_time(self.current_pos)
        step_num = (self.current_pos - self.range_start) // self.step_ms + 1
        vname = os.path.basename(self.video_path)
        for qi, q in enumerate(self.questions):
            rec = {"video":vname,"label":self.label,"timestamp":ts,"step":step_num,"question":q,"answer":self.answers_buf.get(qi,"")}
            self.records.append(rec)
            self._add_table_row(rec)
        self.btn_export.setEnabled(True)

    def _add_table_row(self, rec):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setRowHeight(row, 32)
        is_mother = rec["label"] == "Mother"
        role_clr = QColor(MOTHER_CLR) if is_mother else QColor(CHILD_CLR)

        # 0: Video
        item_v = QTableWidgetItem(rec["video"])
        item_v.setForeground(QColor(TEXT_SECONDARY))
        self.table.setItem(row, 0, item_v)

        # 1: Label (Role tag with bold colored text)
        item_l = QTableWidgetItem(rec["label"])
        item_l.setForeground(role_clr)
        f = item_l.font()
        f.setBold(True)
        item_l.setFont(f)
        item_l.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table.setItem(row, 1, item_l)

        # 2: Timestamp
        item_t = QTableWidgetItem(rec["timestamp"])
        item_t.setForeground(QColor(ACCENT2))
        item_t.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table.setItem(row, 2, item_t)

        # 3: Step #
        item_s = QTableWidgetItem(str(rec["step"]))
        item_s.setForeground(QColor("#a5b4fc"))
        item_s.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table.setItem(row, 3, item_s)

        # 4: Question
        item_q = QTableWidgetItem(rec["question"])
        item_q.setForeground(QColor(TEXT_MAIN))
        self.table.setItem(row, 4, item_q)

        # 5: Answer
        item_a = QTableWidgetItem(rec["answer"])
        item_a.setForeground(QColor(TEXT_MAIN))
        self.table.setItem(row, 5, item_a)

        self.table.scrollToBottom()

    def _advance_step(self):
        self.current_pos += self.step_ms
        if self.current_pos >= self.range_end:
            self._finish_processing(); return
        self.player.setPosition(self.current_pos)
        self.player.play()
        QTimer.singleShot(500, self._begin_step)

    def _finish_processing(self):
        self.processing = False
        self.player.pause()
        self.btn_start.setEnabled(True); self.btn_stop.setEnabled(False)
        self.ans_input.setEnabled(False); self.btn_next_q.setEnabled(False); self.btn_skip_q.setEnabled(False)
        if hasattr(self, 'floating_hud') and self.floating_hud:
            self.floating_hud.hud_ans_input.setEnabled(False)
            self.floating_hud.hud_btn_next.setEnabled(False)
            self.floating_hud.hud_btn_skip.setEnabled(False)
            self.floating_hud.hud_q_text.setText("(processing complete)")
            self.floating_hud.hud_q_counter.setText("Done!")
        self.q_text.setText("(processing complete)")
        self.q_counter.setText("Done!")
        self._set_status(f"✅ Finished! {len(self.records)} records. Ready to export.")
        if self.is_fullscreen:
            self._toggle_fullscreen()
        QMessageBox.information(self,"Done",f"Processing complete!\n{len(self.records)} annotation records collected.")

    def _stop_processing(self):
        if not self.processing: return
        self.processing = False; self.waiting_ans = False
        self.player.pause()
        self.btn_start.setEnabled(True); self.btn_stop.setEnabled(False)
        self.ans_input.setEnabled(False); self.btn_next_q.setEnabled(False); self.btn_skip_q.setEnabled(False)
        if hasattr(self, 'floating_hud') and self.floating_hud:
            self.floating_hud.hud_ans_input.setEnabled(False)
            self.floating_hud.hud_btn_next.setEnabled(False)
            self.floating_hud.hud_btn_skip.setEnabled(False)
        self._set_status("⏹ Processing stopped.")

    # ── Export ─────────────────────────────────────────────────────────────────
    def _export_excel(self):
        if not self.records:
            QMessageBox.warning(self,"No Data","No records to export."); return
        path, _ = QFileDialog.getSaveFileName(self,"Save Excel","annotations.xlsx","Excel Files (*.xlsx)")
        if not path: return
        if OPENPYXL_AVAILABLE:
            self._export_openpyxl(path)
        else:
            path2 = path.replace(".xlsx",".csv")
            with open(path2,"w",newline="",encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=["video","label","timestamp","step","question","answer"])
                w.writeheader(); w.writerows(self.records)
            QMessageBox.information(self,"Exported (CSV)",f"openpyxl not found — saved as CSV:\n{path2}")

    def _export_openpyxl(self, path):
        wb = Workbook(); ws = wb.active; ws.title = "Annotations"
        headers = ["Video Title","Label","Timestamp","Step #","Question","Answer"]
        hfill = PatternFill("solid", fgColor="35355A")
        hfont = Font(bold=True, color="E0E0F0", size=12)
        bs = Side(style="thin", color="555577")
        brd = Border(left=bs,right=bs,top=bs,bottom=bs)
        for c,h in enumerate(headers,1):
            cell = ws.cell(1,c,h); cell.font=hfont; cell.fill=hfill
            cell.alignment=Alignment(horizontal="center",vertical="center"); cell.border=brd
        ws.row_dimensions[1].height = 22
        for r,rec in enumerate(self.records,2):
            is_mother = rec["label"]=="Mother"
            fill = PatternFill("solid",fgColor="3D2A10" if is_mother else "0D2E2A")
            lclr = "F4A261" if is_mother else "56CFB2"
            for c,val in enumerate([rec["video"],rec["label"],rec["timestamp"],rec["step"],rec["question"],rec["answer"]],1):
                cell = ws.cell(r,c,val); cell.fill=fill; cell.border=brd
                cell.alignment=Alignment(vertical="center",wrap_text=True)
                if c==2: cell.font=Font(bold=True,color=lclr)
        for i,w in zip(range(1,7),[35,10,12,8,55,65]):
            ws.column_dimensions[ws.cell(1,i).column_letter].width=w
        ws.freeze_panes="A2"
        wb.save(path)
        self._set_status(f"✅ Exported: {os.path.basename(path)}")
        QMessageBox.information(self,"Exported",f"Saved to:\n{path}")

    def _clear_table(self):
        if self.records and QMessageBox.question(self,"Clear?","Clear all records?",
            QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            self.records.clear(); self.table.setRowCount(0); self.btn_export.setEnabled(False)
            self._set_status("Table cleared.")

    def _set_status(self, msg):
        self.status_lbl.setText(msg)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Video Annotator")
    win = VideoAnnotator()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()