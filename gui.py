from PySide6.QtWidgets import (
    QMainWindow, QDialog, QWidget, QScrollArea,
    QVBoxLayout, QHBoxLayout, QFormLayout,
    QPushButton, QTextEdit, QLabel, QStatusBar, QSizeGrip,
    QLineEdit, QSpinBox, QDialogButtonBox, QFrame, QMessageBox,
)
from PySide6.QtCore import Qt, QDateTime, QPoint
from PySide6.QtGui import QFont, QTextCursor

from winotify import Notification
from alert import MonitorThread
from config import load_config, save_config


# ════════════════════════════════════════════════════════════════════════════════
#  공용 스타일시트
# ════════════════════════════════════════════════════════════════════════════════
DARK_STYLE = """
    QWidget {
        background-color: #1a1a1a;
        color: #cccccc;
        font-family: 'Malgun Gothic', 'Segoe UI', sans-serif;
        font-size: 13px;
    }
    QLineEdit, QSpinBox {
        background-color: #141414;
        color: #d4d4d4;
        border: 1px solid #3a3a3a;
        border-radius: 4px;
        padding: 4px 8px;
        selection-background-color: #264f78;
    }
    QLineEdit:focus, QSpinBox:focus { border-color: #2a5a8a; }
    QSpinBox::up-button, QSpinBox::down-button { width: 0; }
    QLabel#FieldLabel { color: #888888; font-size: 12px; }

    #DialogRoot {
        border: 1px solid #3a3a3a;
        border-radius: 6px;
        background-color: #1a1a1a;
    }
    #RootWidget {
        border: 1px solid #3a3a3a;
        border-radius: 6px;
        background-color: #1a1a1a;
    }
    #TitleBar {
        background-color: #252525;
        border-bottom: 1px solid #333333;
        border-top-left-radius: 5px;
        border-top-right-radius: 5px;
    }
    #TitleLabel { color: #888888; font-size: 12px; letter-spacing: 0.5px; }
    #MinBtn, #MaxBtn {
        background: transparent; color: #777777; border: none; font-size: 14px;
    }
    #MinBtn:hover, #MaxBtn:hover { background-color: #3a3a3a; color: #ffffff; }
    #CloseBtn {
        background: transparent; color: #777777; border: none;
        font-size: 13px; border-top-right-radius: 5px;
    }
    #CloseBtn:hover { background-color: #c0392b; color: #ffffff; }

    #LogView {
        background-color: #141414; color: #d4d4d4;
        border: 1px solid #2e2e2e; border-radius: 4px;
        selection-background-color: #264f78;
    }
    QScrollBar:vertical {
        background: #1e1e1e; width: 8px; border-radius: 4px;
    }
    QScrollBar::handle:vertical {
        background: #3c3c3c; border-radius: 4px; min-height: 20px;
    }
    QScrollBar::handle:vertical:hover { background: #555555; }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }

    /* 브랜치 스크롤 영역 */
    #BranchScroll, #BranchScrollContents {
        background-color: #141414;
        border: none;
    }
    /* 브랜치 행 */
    #BranchRow { background-color: transparent; }
    #BranchEdit {
        background-color: #1e1e1e;
        border: 1px solid #2e2e2e;
        border-radius: 4px;
        color: #d4d4d4;
        padding: 3px 8px;
    }
    #BranchEdit:focus { border-color: #2a5a8a; }
    #BranchDeleteBtn {
        background-color: transparent;
        color: #555555;
        border: none;
        font-size: 16px;
        padding: 0 4px;
    }
    #BranchDeleteBtn:hover { color: #f48771; }
    /* + 버튼 */
    #AddBranchBtn {
        background-color: #1e2a1e;
        color: #4ec9b0;
        border: 1px dashed #2e4e3e;
        border-radius: 4px;
        padding: 4px 0;
        font-size: 13px;
    }
    #AddBranchBtn:hover {
        background-color: #243224;
        border-color: #4ec9b0;
        color: #6edcbe;
    }

    #ActionBtn {
        background-color: #2d2d2d; color: #aaaaaa;
        border: 1px solid #3a3a3a; border-radius: 4px; padding: 5px 0;
    }
    #ActionBtn:hover { background-color: #383838; color: #cccccc; border-color: #555555; }
    #ActionBtn:pressed { background-color: #222222; }
    #PrimaryBtn {
        background-color: #1f4068; color: #7ec8e3;
        border: 1px solid #2a5a8a; border-radius: 4px;
        padding: 5px 0; font-weight: bold;
    }
    #PrimaryBtn:hover { background-color: #2a5a8a; color: #aaddee; }
    #PrimaryBtn:pressed { background-color: #163050; }
    #PrimaryBtn:checked { background-color: #4a1a1a; color: #f48771; border-color: #7a2a2a; }
    #PrimaryBtn:checked:hover { background-color: #5a2222; }

    QDialogButtonBox QPushButton {
        background-color: #2d2d2d; color: #aaaaaa;
        border: 1px solid #3a3a3a; border-radius: 4px;
        padding: 5px 18px; min-width: 70px;
    }
    QDialogButtonBox QPushButton:hover {
        background-color: #383838; color: #cccccc; border-color: #555555;
    }
    QDialogButtonBox QPushButton[text="확인"] {
        background-color: #1f4068; color: #7ec8e3;
        border-color: #2a5a8a; font-weight: bold;
    }
    QDialogButtonBox QPushButton[text="확인"]:hover { background-color: #2a5a8a; }

    #MyStatusBar {
        background-color: #1f1f1f; color: #555555;
        border-top: 1px solid #2e2e2e; font-size: 11px;
    }
    #InfoLabel { color: #666666; font-size: 12px; }
    #InfoLabel b { color: #999999; }
"""


# ════════════════════════════════════════════════════════════════════════════════
#  커스텀 타이틀바
# ════════════════════════════════════════════════════════════════════════════════
class TitleBar(QWidget):
    def __init__(self, parent, title: str, closable=True, maximizable=True):
        super().__init__(parent)
        self._win = parent
        self._drag_pos = QPoint()
        self._dragging = False
        self._btn_max = None

        self.setFixedHeight(36)
        self.setObjectName("TitleBar")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 6, 0)
        layout.setSpacing(0)

        lbl = QLabel(f"  {title}")
        lbl.setObjectName("TitleLabel")
        layout.addWidget(lbl)
        layout.addStretch()

        buttons = [("MinBtn", "─", self._minimize)]
        if maximizable:
            buttons.append(("MaxBtn", "□", self._toggle_max))
        if closable:
            buttons.append(("CloseBtn", "✕", self._win.close))

        for name, symbol, slot in buttons:
            btn = QPushButton(symbol)
            btn.setObjectName(name)
            btn.setFixedSize(40, 36)
            btn.setCursor(Qt.ArrowCursor)
            btn.clicked.connect(slot)
            layout.addWidget(btn)
            if name == "MaxBtn":
                self._btn_max = btn

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._dragging = True
            self._drag_pos = e.globalPosition().toPoint() - self._win.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        if self._dragging and e.buttons() == Qt.LeftButton:
            if hasattr(self._win, 'isMaximized') and self._win.isMaximized():
                self._win.showNormal()
                if self._btn_max: self._btn_max.setText("□")
                self._drag_pos = QPoint(self._win.width() // 2, 18)
            self._win.move(e.globalPosition().toPoint() - self._drag_pos)

    def mouseReleaseEvent(self, e):
        self._dragging = False

    def mouseDoubleClickEvent(self, e):
        if e.button() == Qt.LeftButton and self._btn_max:
            self._toggle_max()

    def _minimize(self): self._win.showMinimized()

    def _toggle_max(self):
        if self._win.isMaximized():
            self._win.showNormal()
            if self._btn_max: self._btn_max.setText("□")
        else:
            self._win.showMaximized()
            if self._btn_max: self._btn_max.setText("❐")


# ════════════════════════════════════════════════════════════════════════════════
#  8방향 리사이즈 베이스
# ════════════════════════════════════════════════════════════════════════════════
class ResizableWindow(QMainWindow):
    MARGIN = 6

    def __init__(self):
        super().__init__()
        self._resize_dir = None
        self._drag_start_pos = QPoint()
        self._drag_start_geom = None
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setMouseTracking(True)
        self.setMinimumSize(680, 480)

    def _get_dir(self, pos):
        m, w, h = self.MARGIN, self.width(), self.height()
        x, y = pos.x(), pos.y()
        L, R, T, B = x < m, x > w-m, y < m, y > h-m
        if T and L: return "TL"
        if T and R: return "TR"
        if B and L: return "BL"
        if B and R: return "BR"
        if L: return "L"
        if R: return "R"
        if T: return "T"
        if B: return "B"
        return None

    def _cursor(self, d):
        return {
            "L": Qt.SizeHorCursor,   "R": Qt.SizeHorCursor,
            "T": Qt.SizeVerCursor,   "B": Qt.SizeVerCursor,
            "TL": Qt.SizeFDiagCursor,"BR": Qt.SizeFDiagCursor,
            "TR": Qt.SizeBDiagCursor,"BL": Qt.SizeBDiagCursor,
        }.get(d, Qt.ArrowCursor)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton and not self.isMaximized():
            d = self._get_dir(e.position().toPoint())
            if d:
                self._resize_dir = d
                self._drag_start_pos = e.globalPosition().toPoint()
                self._drag_start_geom = self.geometry()

    def mouseMoveEvent(self, e):
        if not self.isMaximized():
            if self._resize_dir:
                self._do_resize(e.globalPosition().toPoint())
            else:
                d = self._get_dir(e.position().toPoint())
                self.setCursor(self._cursor(d) if d else Qt.ArrowCursor)

    def mouseReleaseEvent(self, e):
        self._resize_dir = None
        self.setCursor(Qt.ArrowCursor)

    def _do_resize(self, gpos):
        dx = gpos.x() - self._drag_start_pos.x()
        dy = gpos.y() - self._drag_start_pos.y()
        g  = self._drag_start_geom
        d  = self._resize_dir
        x, y, w, h = g.x(), g.y(), g.width(), g.height()
        if "L" in d: x += dx; w -= dx
        if "R" in d: w += dx
        if "T" in d: y += dy; h -= dy
        if "B" in d: h += dy
        mw, mh = self.minimumWidth(), self.minimumHeight()
        if w < mw: x = g.right() - mw; w = mw
        if h < mh: y = g.bottom() - mh; h = mh
        self.setGeometry(x, y, w, h)


# ════════════════════════════════════════════════════════════════════════════════
#  브랜치 입력 한 행
# ════════════════════════════════════════════════════════════════════════════════
class BranchRow(QWidget):
    def __init__(self, value: str = "", on_delete=None, parent=None):
        super().__init__(parent)
        self._on_delete = on_delete
        self.setObjectName("BranchRow")
        self.setFixedHeight(32)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 2, 0, 2)
        layout.setSpacing(6)

        # 브랜치 아이콘 레이블
        icon = QLabel("⎇")
        icon.setFixedWidth(18)
        icon.setStyleSheet("color: #555555; font-size: 13px;")
        icon.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon)

        self.edit = QLineEdit(value)
        self.edit.setObjectName("BranchEdit")
        self.edit.setPlaceholderText("브랜치 이름 (예: master)")
        layout.addWidget(self.edit)

        self.btn_del = QPushButton("×")
        self.btn_del.setObjectName("BranchDeleteBtn")
        self.btn_del.setFixedSize(24, 24)
        self.btn_del.setCursor(Qt.ArrowCursor)
        self.btn_del.clicked.connect(lambda: self._on_delete(self) if self._on_delete else None)
        layout.addWidget(self.btn_del)

    def value(self) -> str:
        return self.edit.text().strip()


# ════════════════════════════════════════════════════════════════════════════════
#  브랜치 목록 에디터 (스크롤 + 동적 추가)
# ════════════════════════════════════════════════════════════════════════════════
class BranchEditor(QWidget):
    def __init__(self, branches: list[str], parent=None):
        super().__init__(parent)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(4)

        # 헤더 (레이블 + + 버튼)
        header = QHBoxLayout()
        lbl = QLabel("브랜치 목록")
        lbl.setObjectName("FieldLabel")
        header.addWidget(lbl)
        header.addStretch()
        btn_add = QPushButton("＋  브랜치 추가")
        btn_add.setObjectName("AddBranchBtn")
        btn_add.setFixedHeight(26)
        btn_add.setFixedWidth(120)
        btn_add.setCursor(Qt.ArrowCursor)
        btn_add.clicked.connect(lambda: self.add_row())
        header.addWidget(btn_add)
        outer.addLayout(header)

        # 스크롤 영역
        self._scroll = QScrollArea()
        self._scroll.setObjectName("BranchScroll")
        self._scroll.setWidgetResizable(True)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._scroll.setFixedHeight(140)
        self._scroll.setFrameShape(QFrame.NoFrame)

        self._contents = QWidget()
        self._contents.setObjectName("BranchScrollContents")
        self._rows_layout = QVBoxLayout(self._contents)
        self._rows_layout.setContentsMargins(6, 4, 6, 4)
        self._rows_layout.setSpacing(2)
        self._rows_layout.addStretch()   # 행들이 위쪽에 쌓이도록

        self._scroll.setWidget(self._contents)
        outer.addWidget(self._scroll)

        self._rows: list[BranchRow] = []

        # 초기값 로드
        for b in (branches or ["master"]):
            self.add_row(b)

    def add_row(self, value: str = ""):
        row = BranchRow(value, on_delete=self.remove_row, parent=self._contents)
        # stretch 앞에 삽입
        idx = self._rows_layout.count() - 1
        self._rows_layout.insertWidget(idx, row)
        self._rows.append(row)
        # 스크롤 최하단으로
        self._scroll.verticalScrollBar().setValue(
            self._scroll.verticalScrollBar().maximum()
        )
        if not value:
            row.edit.setFocus()

    def remove_row(self, row: BranchRow):
        if len(self._rows) <= 1:
            return   # 최소 1개 유지 (버튼으로 삭제 시)
        self._force_remove(row)

    def _force_remove(self, row: BranchRow):
        self._rows.remove(row)
        self._rows_layout.removeWidget(row)
        row.deleteLater()

    def clear_rows(self):
        for row in list(self._rows):
            self._force_remove(row)

    def values(self) -> list[str]:
        return [r.value() for r in self._rows if r.value()]


# ════════════════════════════════════════════════════════════════════════════════
#  설정 다이얼로그
# ════════════════════════════════════════════════════════════════════════════════
class SetupDialog(QDialog):
    def __init__(self, cfg: dict, parent=None):
        super().__init__(parent, Qt.FramelessWindowHint | Qt.Dialog)
        self._cfg = cfg
        self.setMinimumWidth(460)
        self.setStyleSheet(DARK_STYLE)
        self._init_ui()
        self._load(cfg)

    def _init_ui(self):
        root = QWidget()
        root.setObjectName("DialogRoot")
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(root)

        layout = QVBoxLayout(root)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(TitleBar(self, "연결 설정", maximizable=False))

        form_container = QWidget()
        form_layout = QVBoxLayout(form_container)
        form_layout.setContentsMargins(24, 16, 24, 16)
        form_layout.setSpacing(12)

        form = QFormLayout()
        form.setSpacing(10)
        form.setLabelAlignment(Qt.AlignRight)

        def lbl(text):
            l = QLabel(text)
            l.setObjectName("FieldLabel")
            return l

        self.edit_url     = QLineEdit()
        self.edit_url.setPlaceholderText("https://bitbucket.example.com")
        self.edit_project = QLineEdit()
        self.edit_project.setPlaceholderText("PROJECT")
        self.edit_repo    = QLineEdit()
        self.edit_repo.setPlaceholderText("my-repo")
        self.edit_token   = QLineEdit()
        self.edit_token.setPlaceholderText("Bearer 토큰")
        self.edit_token.setEchoMode(QLineEdit.Password)
        self.spin_interval = QSpinBox()
        self.spin_interval.setRange(10, 3600)
        self.spin_interval.setSuffix("  초")

        form.addRow(lbl("Bitbucket URL"), self.edit_url)
        form.addRow(lbl("Project Key"),   self.edit_project)
        form.addRow(lbl("Repository"),    self.edit_repo)
        form.addRow(lbl("Access Token"),  self.edit_token)
        form.addRow(lbl("폴링 주기"),      self.spin_interval)

        form_layout.addLayout(form)

        # 구분선
        div = QFrame()
        div.setFrameShape(QFrame.HLine)
        div.setStyleSheet("color: #2e2e2e;")
        form_layout.addWidget(div)

        # 브랜치 에디터 (초기엔 빈 리스트, _load에서 채움)
        self._branch_editor = BranchEditor([], parent=self)
        form_layout.addWidget(self._branch_editor)

        # OK / Cancel
        btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btn_box.button(QDialogButtonBox.Ok).setText("확인")
        btn_box.button(QDialogButtonBox.Cancel).setText("취소")
        btn_box.accepted.connect(self._on_accept)
        btn_box.rejected.connect(self.reject)
        form_layout.addWidget(btn_box)

        layout.addWidget(form_container)

    def _load(self, cfg: dict):
        self.edit_url.setText(cfg.get("url", ""))
        self.edit_project.setText(cfg.get("project", ""))
        self.edit_repo.setText(cfg.get("repo", ""))
        self.edit_token.setText(cfg.get("token", ""))
        self.spin_interval.setValue(cfg.get("polling_interval", 60))
        branches = cfg.get("branches", ["master"])
        # 기존 행 전체 제거 후 재구성
        self._branch_editor.clear_rows()
        for b in branches:
            self._branch_editor.add_row(b)

    def _on_accept(self):
        missing = []
        if not self.edit_url.text().strip():     missing.append("Bitbucket URL")
        if not self.edit_project.text().strip(): missing.append("Project Key")
        if not self.edit_repo.text().strip():    missing.append("Repository")
        if not self.edit_token.text().strip():   missing.append("Access Token")
        branches = self._branch_editor.values()
        if not branches: missing.append("브랜치 (최소 1개)")
        if missing:
            QMessageBox.warning(
                self, "입력 오류",
                "필수 항목을 입력해주세요:\n• " + "\n• ".join(missing)
            )
            return
        self._cfg.update({
            "url":              self.edit_url.text().strip(),
            "project":          self.edit_project.text().strip(),
            "repo":             self.edit_repo.text().strip(),
            "token":            self.edit_token.text().strip(),
            "branches":         branches,
            "polling_interval": self.spin_interval.value(),
        })
        save_config(self._cfg)
        self.accept()

    def get_config(self) -> dict:
        return self._cfg


# ════════════════════════════════════════════════════════════════════════════════
#  메인 윈도우
# ════════════════════════════════════════════════════════════════════════════════
class MainWindow(ResizableWindow):
    def __init__(self, cfg: dict):
        super().__init__()
        self._cfg = cfg
        self.thread = None
        self._init_ui()
        self.setStyleSheet(DARK_STYLE)
        self._refresh_info()

    def _init_ui(self):
        root_widget = QWidget()
        root_widget.setObjectName("RootWidget")
        self.setCentralWidget(root_widget)

        root_layout = QVBoxLayout(root_widget)
        root_layout.setContentsMargins(1, 1, 1, 1)
        root_layout.setSpacing(0)

        root_layout.addWidget(TitleBar(self, "Bitbucket Push Monitor"))

        body = QWidget()
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(12, 8, 12, 8)
        body_layout.setSpacing(8)
        root_layout.addWidget(body)

        info_bar = QHBoxLayout()
        self.lbl_info = QLabel()
        self.lbl_info.setObjectName("InfoLabel")
        self.lbl_info.setTextFormat(Qt.RichText)
        info_bar.addWidget(self.lbl_info)
        info_bar.addStretch()

        self.btn_settings = QPushButton("⚙  설정")
        self.btn_settings.setObjectName("ActionBtn")
        self.btn_settings.setFixedWidth(80)
        self.btn_settings.clicked.connect(self._open_settings)
        info_bar.addWidget(self.btn_settings)
        body_layout.addLayout(info_bar)

        self.log_view = QTextEdit()
        self.log_view.setObjectName("LogView")
        self.log_view.setReadOnly(True)
        self.log_view.setFont(QFont("Consolas", 10))
        body_layout.addWidget(self.log_view)

        btn_bar = QHBoxLayout()
        btn_bar.addStretch()

        self.btn_clear = QPushButton("로그 지우기")
        self.btn_clear.setObjectName("ActionBtn")
        self.btn_clear.setFixedWidth(100)
        self.btn_clear.clicked.connect(self.log_view.clear)

        self.btn_toggle = QPushButton("▶  시작")
        self.btn_toggle.setObjectName("PrimaryBtn")
        self.btn_toggle.setFixedWidth(110)
        self.btn_toggle.setCheckable(True)
        self.btn_toggle.clicked.connect(self._toggle_monitor)

        btn_bar.addWidget(self.btn_clear)
        btn_bar.addWidget(self.btn_toggle)
        body_layout.addLayout(btn_bar)

        self.status_bar = QStatusBar()
        self.status_bar.setObjectName("MyStatusBar")
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("대기 중")
        self.status_bar.addPermanentWidget(QSizeGrip(self))

    def _refresh_info(self):
        cfg = self._cfg
        branches_str = ", ".join(cfg.get("branches", []))
        self.lbl_info.setText(
            f"저장소: <b>{cfg.get('repo', '-')}</b> &nbsp;|&nbsp; "
            f"브랜치: <b>{branches_str}</b> &nbsp;|&nbsp; "
            f"주기: <b>{cfg.get('polling_interval', 60)}s</b>"
        )

    def _open_settings(self):
        if self.thread:
            self._stop_monitor()
        dlg = SetupDialog(self._cfg, parent=self)
        if dlg.exec() == QDialog.Accepted:
            self._cfg = dlg.get_config()
            self._refresh_info()
            self._append_log("── 설정이 저장되었습니다 ──")

    def _toggle_monitor(self, checked: bool):
        self._start_monitor() if checked else self._stop_monitor()

    def _start_monitor(self):
        self.thread = MonitorThread(self._cfg)
        self.thread.log.connect(self._append_log)
        self.thread.alert.connect(self._show_alert)
        self.thread.start()
        self.btn_toggle.setText("■  중지")
        self.status_bar.showMessage("감시 중…")

    def _stop_monitor(self):
        if self.thread:
            self.thread.stop()
            self.thread.wait()
            self.thread = None
        self.btn_toggle.setText("▶  시작")
        self.btn_toggle.setChecked(False)
        self.status_bar.showMessage("중지됨")
        self._append_log("── 감시 중지 ──")

    def _append_log(self, message: str):
        timestamp = QDateTime.currentDateTime().toString("HH:mm:ss")
        if "새 커밋 감지" in message:   color = "#4ec9b0"
        elif "실패" in message or "오류" in message: color = "#f48771"
        elif "──" in message:           color = "#555555"
        else:                           color = "#d4d4d4"
        self.log_view.moveCursor(QTextCursor.End)
        self.log_view.insertHtml(
            f'<span style="color:#555555;">[{timestamp}]</span> '
            f'<span style="color:{color};">{message}</span><br>'
        )
        self.log_view.moveCursor(QTextCursor.End)

    def _show_alert(self, title: str, body: str):
        Notification(app_id="GitAlert", title=title, msg=body, duration="short").show()

    def closeEvent(self, event):
        self._stop_monitor()
        event.accept()
